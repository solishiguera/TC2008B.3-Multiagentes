using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

 public class Coordinate
 {
    public int x;
    public int y;

    public Coordinate(int x, int y)
    {
        this.x= x;
        this.y = y;
    }
 }

  public class Car
 {
    public int id;
    public List<Coordinate> ruta;

    public Car(int id)
    {
        this.id= id;
        this.ruta = new List<Coordinate>();;
    }

    public Car(int id, List<Coordinate> ruta)
    {
        this.id= id;
        this.ruta = ruta;
    }

    public void addStep(Coordinate step)
    {
        ruta.Add(step);
    }
 }

public class readfromMesa : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        // A correct website page.
        //StartCoroutine(GetRequest("http://127.0.0.1:5000/cars"));
    }

    IEnumerator GetRequest(string uri)
    {
       UnityWebRequest www = UnityWebRequest.Get(uri);
        yield return www.Send();
 
        if(www.isNetworkError) {
            Debug.Log(www.error);
        }
        else {
            // Guardamos la cadena de texto completo
            
            string text = www.downloadHandler.text.Replace(" ", "");
            //Debug.Log(text);
            text = text.Replace("\"", "");
            text = text.Replace(",", "");

            // Como no hay un parser en unity que nos sirva, haremos nuestro propio parser
            text = text.Replace("u", "");
            text = text.Replace("n", "");
            text = text.Replace("i", "");
            text = text.Replace("u", "");
            text = text.Replace("d", "");
            text = text.Replace("e", "");
            text = text.Replace("o", "");
            text = text.Replace("s", "");
            text = text.Replace(":", "");
            text = text.Replace("{", "");
            text = text.Replace("}", "");
            text = text.Replace("[", "");
            text = text.Replace("]", "");
            text = text.Replace("_", "");
            //Debug.Log(www.downloadHandler.text);
            Debug.Log(text);
            
            List<Car> carsNroutes = new List<Car>();

            int carCounter = -1;

            for (int i = 0; i <= text.Length-2; i++){
                if(text[i] == 'q'){
                    i += 5;
                    Car tempCar = new Car(i);
                    carCounter++;
                    carsNroutes.Add(tempCar);
                }else {
                    Coordinate tempCord = new Coordinate(text[i]- '0', text[i+1]- '0');
                    i++;
                    carsNroutes[carCounter].addStep(tempCord);
                }
            }
            Debug.Log("Despues del parser");
            Debug.Log("Cant carros: " + carsNroutes.Count);
            Debug.Log("Coordenadas del primer carro:");
            for(int i = 0; i < 10; i++){
                Debug.Log("(" + carsNroutes[0].ruta[i].x + "," +  carsNroutes[0].ruta[i].y + ")");
            }
            
            
        }
    }
}
