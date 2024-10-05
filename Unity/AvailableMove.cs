using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AvailableMove : MonoBehaviour
{
    public int x, y;
    public char colour;

    public void setPos(int x, int y) {
        this.x = x;
        this.y = y;

        transform.position = new Vector3((8.75f - (2.5f*y)), 0.25f, (-8.75f + (2.5f*x)));
    }

    void OnMouseDown() {
        FindObjectOfType<Game>().MakeMove(x, y);
    }
}
