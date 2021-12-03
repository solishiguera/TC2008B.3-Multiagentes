using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class WP_Actor : MonoBehaviour
{
    float speed = 5.0f;
    public Transform target;

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
        GameObject.Find ("Semaforo4").GetComponent<Renderer>().material = green;
        StartCoroutine(GetRequest("http://127.0.0.1:5000/car3"));
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
            timetoWait = 0;
        }
    }

    // Update is called once per frame
    void Update()
    {
        transform.Translate(new Vector3(0,0,speed * Time.deltaTime));

        if(advance){
            timetoWait -= Time.deltaTime;
            if(timetoWait < -4 && timetoWait > -5){
                GameObject.Find ("Semaforo4").GetComponent<Renderer>().material = yellow;
            }else if(timetoWait < -7){
                GameObject.Find ("Semaforo4").GetComponent<Renderer>().material = red;
            }
        }
        
    }

    void OnTriggerEnter(Collider other){
        Debug.Log("Si choco");
        if(other.tag == "WP_Red"){
            target = other.gameObject.GetComponent<Waypoint>().nextPoint;
            Vector3 lookAtPosition = target.position;
            lookAtPosition.y = transform.position.x;
            transform.LookAt(new Vector3(target.position.x, transform.position.y, target.position.z));
        }

        if(other.tag == "SemaforoAdmin"){
            if(timetoWait > 0){
                advance = false;
            }
        }
    }
}
