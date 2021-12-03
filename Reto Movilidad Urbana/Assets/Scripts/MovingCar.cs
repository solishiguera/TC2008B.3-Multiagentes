using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MovingCar : MonoBehaviour
{
    // Paso 0.
    Vector3[] points;
    float angle;  // <------
    
    private Vector4 homogenise(Vector3 point)
    {
        return new Vector4(point.x, point.y, point.z, 1);
    }
    
    private Vector3 dehomogenise(Vector4 point)
    {
        return new Vector3(point.x, point.y, point.z);
    }
    
    void TransformCar()
    {
        // Paso 2. Ya no hay tres puntos    
        int n = points.Length;
        Vector3[] vertices = new Vector3[n];
        for (int i = 0; i < n; i++)
        {
            vertices[i] = points[i];
            // vertices.w = 1.0f;
        }

        // Transformation matrices (solo rotar)
        Matrix4x4 rotation1 = Transformations.RotateM(angle, Transformations.AXIS.AX_Y);
        
        Matrix4x4 transfMatrix = rotation1;
        
        // Apply transformation
        for (int i = 0; i < n; i++)
        {
            vertices[i] = dehomogenise(transfMatrix * homogenise(vertices[i]));
        }

        GetComponent<MeshFilter>().mesh.vertices = vertices;
    }

    // Start is called before the first frame update
    void Start()
    {
        // Paso 1.
        angle = 0;
        Mesh mesh = GetComponent<MeshFilter>().mesh;
        
        // Geometry
        points = mesh.vertices;
    }

    // Update is called once per frame
    void Update()
    {
        angle += 1.0f;
        TransformCar();
    }
}
