using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Disc : MonoBehaviour
{
    public int x, y;
    public char colour = 'B';

    void Awake() {
        colour = 'B';
        gameObject.tag = "DarkDisc";
    }
 
    public void SetPos(int x, int y) {
        this.x = x;
        this.y = y;

        transform.position = new Vector3((8.75f - (2.5f*y)), 0.75f, (-8.75f + (2.5f*x)));
    }

    public void flip() {
        transform.position += new Vector3(0f, 0.75f, 0f);

        if (this.colour == 'B') {
            transform.rotation = new Quaternion(180, 0, 0, 0);
            this.colour = 'W';
            gameObject.tag = "LightDisc";
        } else {
            transform.rotation = new Quaternion(0, 0, 0, 0);
            this.colour = 'B';
            gameObject.tag = "DarkDisc";
        }
    }
}