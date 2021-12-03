from flask import Flask, json
# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 

from mesa import Agent, Model 

# Debido a que necesitamos varios agentes por celda elegimos `MultiGrid` ya que en casos tendremos varios agentes en una celda.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation


from mesa.datacollection import DataCollector



import numpy as np
import pandas as pd


import time
import datetime
import math
import random
import json

def get_grid(model):
    '''
    Esta es una función auxiliar que nos permite guardar el grid para cada uno de los agentes.
    param model: El modelo del cual optener el grid.
    return una matriz con la información del grid del agente.
    '''
    grid = np.ones((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        for obj in cell_content:
          if isinstance(obj, Carro):
            grid[x][y] = 30
          elif isinstance(obj,Diseño):
                grid[x][y] = 100
          elif isinstance(obj, adminSem):
                grid[x][y] = 0
          elif isinstance(obj, Semaforo):
              if obj.colorSem == 0: 
                  grid[x][y] = 50
              elif obj.colorSem == 1:
                grid[x][y] = 90
              elif obj.colorSem == 2:
                grid[x][y] = 70
          else: 
                grid[x][y] = 10  
    return grid

class Diseño(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id,model)

class Semaforo(Agent):
    def __init__(self, unique_id, myTurn,color, model):
        super().__init__(unique_id,model)
        self.myTurn = myTurn
        self.colorSem = color # 0 es verde, 1 rojo, 2 es amarillo es no hay carro

    def step(self):
        if self.myTurn == self.model.turnoCalle:
          self.colorSem = 0  #Si es su turno se cambia a verde

class Carro(Agent):
    def __init__(self, unique_id, direccion, model):
        super().__init__(unique_id, model)
        self.pos
        self.direccion = direccion # 0 izquierda, 1 derecha, 2 arriba, 3 abajo
        self.stop = False
        self.timestop = 0

    
    def sigMov(self):
        if self.pos[1] == model.width -1 and self.direccion == 1:
          sigPos = (8,0)
          return sigPos
        if self.pos[0] == model.height -1 and self.direccion == 3:
          sigPos = (0,6)
          return sigPos
        sigPos = (0,0)

        # La direccion siempre sera la misma por la naturaleza de nuestro codigo, por lo que podemos dictar su sig mov
        if self.direccion == 0:
            sigPos = (self.pos[0], self.pos[1] - 1)
        elif self.direccion == 1:
            sigPos = (self.pos[0], self.pos[1] + 1)
        elif self.direccion == 2:
            sigPos = (self.pos[0] - 1 , self.pos[1])
        elif self.direccion == 3:
            sigPos = (self.pos[0] + 1, self.pos[1])
        return sigPos
 
    def step(self):
        thisCell = self.model.grid.get_cell_list_contents([self.pos])
        checkeoLuz = len([obj for obj in thisCell if isinstance(obj,adminSem)])
        if checkeoLuz > 0:
          #checamos que semaforo le corresponde checar
          if self.direccion == 0:
             celdaVecina = self.model.grid.get_cell_list_contents([(7,5)])
             semaforoCheck = [obj for obj in celdaVecina if isinstance(obj, Semaforo)]
          if self.direccion == 1:
             celdaVecina = self.model.grid.get_cell_list_contents([(7,9)])
             semaforoCheck = [obj for obj in celdaVecina if isinstance(obj, Semaforo)]
          if self.direccion == 2:
             celdaVecina = self.model.grid.get_cell_list_contents([(5,7)])
             semaforoCheck = [obj for obj in celdaVecina if isinstance(obj, Semaforo)]
          if self.direccion == 3:
             celdaVecina = self.model.grid.get_cell_list_contents([(9,7)])
             semaforoCheck = [obj for obj in celdaVecina if isinstance(obj, Semaforo)]
          
          #ahora checamos el semaforo, para saber si sigue avanzando o no
          if semaforoCheck[0].colorSem == 1 or semaforoCheck[0].colorSem == 2:
            self.stop = True
            self.timestop += 1
          else: 
            self.stop = False

        if not self.stop:
          sigPos = self.sigMov()
          thisCell = self.model.grid.get_cell_list_contents([sigPos])
          ##nos aseguramos que no tenga carros delante de el para no chocar en el semaforo
          cantCarros = len([obj for obj in thisCell if isinstance(obj,Carro)])
          if cantCarros == 0:
            self.model.grid.move_agent(self,sigPos)

    
class adminSem(Agent):
    def __init__(self,unique_id, number, model):
        super().__init__(unique_id,model)
        self.hasCarro = False
        self.cont = 0
        self.miSemaforo = number 
        self.startTime = time.time()
    
    def cambioTurno(self):
        if self.model.turnoCalle == 3:
            self.model.turnoCalle = 0
        else:
            self.model.turnoCalle += 1    

    def step(self):
        thisCell = self.model.grid.get_cell_list_contents([self.pos])
        currCarros = len([obj for obj in thisCell if isinstance(obj,Carro)])  #checamos si hay carros en ese momento
        #Si tenemos un carro, reseteamos el contador de ciclos sin carros,
        if currCarros > 0: 
            self.cont = 0
            self.hasCarro = True
        #Si no tenemos un carro, agregamos al contador
        else: 
            self.hasCarro = False 
            self.cont += 1

        #Si llego al contador de 5, significa que ya tuvieron tiempo suficiente todos los carros para pasar la calle completa en verde sin chocar, 
        #por lo que podemos cambiar de turno ahora
        if self.cont == 5:
            if self.miSemaforo == 0:
                celdaVecina = self.model.grid.get_cell_list_contents([(7,5)])
                semaforoCheck = [obj for obj in celdaVecina if isinstance(obj, Semaforo)]
                semaforoCheck[0].colorSem = 1
                self.cambioTurno()
            if self.miSemaforo == 1:
                celdaVecina = self.model.grid.get_cell_list_contents([(7,9)])
                semaforoCheck = [obj for obj in celdaVecina if isinstance(obj, Semaforo)]
                semaforoCheck[0].colorSem = 1
                self.cambioTurno()
            if self.miSemaforo == 2:
                celdaVecina = self.model.grid.get_cell_list_contents([(5,7)])
                semaforoCheck = [obj for obj in celdaVecina if isinstance(obj, Semaforo)]
                semaforoCheck[0].colorSem = 1
                self.cambioTurno()
            if self.miSemaforo == 3:
                celdaVecina = self.model.grid.get_cell_list_contents([(9,7)])
                semaforoCheck = [obj for obj in celdaVecina if isinstance(obj, Semaforo)]
                semaforoCheck[0].colorSem = 1
                self.cambioTurno()
 ##Ahora si hacemos el cruce como tal 
class Cruce:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.turnoCalle = 0 
        #inicializamos los objetos
        
        #Carros

        # Carros que van hacia la izquierda
        carro1 = Carro(2002, 0,self)
        self.schedule.add(carro1)
        self.grid.place_agent(carro1,(6,14))


        # Carros que van hacia la derecha
        carro2 = Carro(2013, 1,self)
        self.schedule.add(carro2)
        self.grid.place_agent(carro2,(8,0))

        
        # Carros que van hacia abajo
        carro3 = Carro(2021, 2,self)
        self.schedule.add(carro3)
        self.grid.place_agent(carro3,(14,8))


        # Carros que van hacia arriba
        carro4 = Carro(2031, 3,self)
        self.schedule.add(carro4)
        self.grid.place_agent(carro4,(0,6))

        #Semaforos
        semaforo_derecho = Semaforo(510,0,2,self)
        self.schedule.add(semaforo_derecho)
        self.grid.place_agent(semaforo_derecho,(7,9))

        semaforo_arriba = Semaforo(511,1,2,self)
        self.schedule.add(semaforo_arriba)
        self.grid.place_agent(semaforo_arriba,(5,7))

        semaforo_abajo = Semaforo(512,2,2,self)
        self.schedule.add(semaforo_abajo)
        self.grid.place_agent(semaforo_abajo,(9,7))

        semaforo_izquierda = Semaforo(513,3,2,self)
        self.schedule.add(semaforo_izquierda)
        self.grid.place_agent(semaforo_izquierda,(7,5))
        
        #Administradores de semaforos
        lc_derecho = adminSem(900, 1, self)
        self.schedule.add(lc_derecho)
        self.grid.place_agent(lc_derecho,(8,5))

        lc_izquierda = adminSem(901, 0, self)
        self.schedule.add(lc_izquierda)
        self.grid.place_agent(lc_izquierda,(6,9))

        lc_abajo = adminSem(902, 3, self)
        self.schedule.add(lc_abajo)
        self.grid.place_agent(lc_abajo, (5,6))

        lc_arriba = adminSem(903, 2, self)
        self.schedule.add(lc_arriba)
        self.grid.place_agent(lc_arriba, (9,8))

        #Diseño del cruce
        contX = 0
        y_v = 5


        # Aquí definimos con colector para obtener el grid completo.
        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

# Definimos el tamaño del Grid
M = 15
N = 15

#Asignamos un tiempo Maximo de ejecucion
MAX_TIME = 0.08

# Registramos el tiempo de inicio y corremos el modelo
tiempoIni = time.time()
model = Cruce(M, N)

maxsteps = 23
stepcounter = 0

while((time.time() - tiempoIni) < MAX_TIME):
    maxsteps -= 1
    model.step()
    if maxsteps < 0:
      break
		
all_grid = model.datacollector.get_model_vars_dataframe()

api = Flask(__name__)

@api.route('/semaforo1', methods=['GET'])
def get_semaforo1(): 
    return str(model.schedule.agents[0].timestop)

@api.route('/semaforo2', methods=['GET'])
def get_semaforo2():
    return str(model.schedule.agents[1].timestop)

@api.route('/semaforo3', methods=['GET'])
def get_semaforo3():
    return str(model.schedule.agents[2].timestop)

@api.route('/semaforo4', methods=['GET'])
def get_semaforo4():
    return str(model.schedule.agents[3].timestop)

if __name__ == '__main__':
    api.run()