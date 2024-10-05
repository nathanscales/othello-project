using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

public class Board : MonoBehaviour
{
    public Disc disc;
    
    private Disc[,] state = new Disc[8,8];
    
    public void SetState(char[,] newState) {
        for(int i = 0; i < newState.GetLength(0); i++) {
            for(int j = 0; j < newState.GetLength(1); j++) {
                if(newState[i, j] != ' ') 
                {
                    PlaceDisc(i, j, newState[i, j]);
                } else {
                    state[i, j] = null;
                }
            }
        }
    }

    public void PlaceDisc(int x, int y, char discColour) {
        Disc d = (this.state[x, y] = Instantiate(this.disc));

        d.SetPos(x, y);

        if (discColour == 'W') {
            d.flip();
        }
    }

    public List<Tile> GetMoves(char playerColour) {
        List<Tile> moves = new List<Tile>();
        List<Disc> playerDiscs = GetDiscs(playerColour);

        foreach(Disc playerDisc in playerDiscs) 
        {
            for(int x=-1; x<=1; x++) {
                for(int y=-1; y<=1; y++) 
                {
                    Disc d;
                    int xPos = playerDisc.x + x;
                    int yPos = playerDisc.y + y;
                    bool seenOpposite = false;

                    while((0 <= xPos && xPos <= 7) && (0 <= yPos && yPos <= 7)) {
                        d = this.state[xPos, yPos];

                        if (d == null) {
                            if (seenOpposite) {
                                moves.Add(new Tile(xPos, yPos));
                            }
                            break;
                        } else if (d.colour == playerColour) {
                            break;
                        } else {
                            seenOpposite = true;
                        }

                        xPos+=x;
                        yPos+=y;

                    }
                }
            }
        }

        return moves;
    }

    public List<Disc> GetDiscs(char colour) {
        List<Disc> discs = new List<Disc>();

        for(int x = 0; x <= 7; x++) {
            for(int y = 0; y <= 7; y++) 
            {
                Disc d = this.state[x, y];

                if(d != null && d.colour == colour) {
                    discs.Add(d);
                }
            }
        }

        return discs;
    }

    public void FlipDiscs(int xStart, int yStart, char playerColour) {
        List<Disc> flipping = new List<Disc>();

        for(int x=-1; x<=1; x++) {
            for(int y=-1; y<=1; y++) 
            {   
                Disc d;
                int xPos = xStart + x;
                int yPos = yStart + y;
                bool seenOpposite = false;

                while((0 <= xPos && xPos <= 7) && (0 <= yPos && yPos <= 7)) {
                    d = this.state[xPos, yPos];

                    if(d == null) {
                        break;
                    } else if (d.colour != playerColour) {
                        seenOpposite = true;
                        flipping.Add(d);
                    } else {
                        if(seenOpposite) {
                            foreach(Disc flip in flipping) {
                                flip.flip();
                            }
                        }
                        break;
                    }

                    xPos+=x;
                    yPos+=y;
                }

                flipping.Clear();
            }
        }
    }
}