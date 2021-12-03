using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ManyCars : MonoBehaviour
{
    public GameObject PrefabCoche; // It must be instantiated
    public int NumeroCoches = 10;

    // Start is called before the first frame update
    void Start()
    {
        for (int i = 0; i < NumeroCoches; i++)
        {
            float x = Random.Range(-40, 40);
            float y = 0; // Todos en el piso
            float z = Random.Range(-40, 40);

            Instantiate(PrefabCoche, new Vector3(x, y, z), 
                Quaternion.Euler(0, 0, 0));
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}