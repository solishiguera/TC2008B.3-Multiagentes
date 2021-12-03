using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class WPBlue_Actor : MonoBehaviour
{
    float speed = 5.0f;
    float timetoWait;
    bool advance = true;

    //Semaforos
    public Renderer semaforo;
    public Material green;
    public Material red;
    public Material yellow;


    // Start is called before the first frame update
    void Start()
    {
        GameObject.Find ("Semaforo2").GetComponent<Renderer>().material = red;
        StartCoroutine(GetRequest("http://127.0.0.1:5000/semaforo1"));
    }

    IEnumerator GetRequest(string uri)
    {
       UnityWebRequest www = UnityWebRequest.Get(uri);
        yield return www.Send();
 
        if(www.isNetworkError) {
            Debug.Log(www.error);
        }
        else {
            timetoWait = float.Parse(www.downloadHandler.text);
            //Debug.Log("From Blue" + timetoWait);

            //De momento para debuggear
            timetoWait = 15;
        }
    }
    
    bool passed = false;

    // Update is called once per frame
    void Update()
    {
        if(advance){
            transform.Translate(new Vector3(0,0,speed * Time.deltaTime));
            if(passed){
                timetoWait -= Time.deltaTime;
                if(timetoWait < -3 && timetoWait > -4){
                    GameObject.Find ("Semaforo2").GetComponent<Renderer>().material = yellow;
                    advance = true;
                }else if( timetoWait < -5){
                    GameObject.Find ("Semaforo2").GetComponent<Renderer>().material = red;
                }
            }
        }else{
            timetoWait -= Time.deltaTime;
            if(timetoWait < 0 && timetoWait > -3){
                Debug.Log("Entre a este");
                GameObject.Find ("Semaforo2").GetComponent<Renderer>().material = green;
                passed = true;
                advance = true;
            }
        }
    }

    void OnTriggerEnter(Collider other){
        if(other.tag == "SemaforoAdmin"){
            advance = false;
            Debug.Log("Choco con semaforo");
        }
    }
}
