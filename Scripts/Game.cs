using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class Game : MonoBehaviour
{
    public TMP_Text txtCurrentTurn, txtDarkDiscs, txtLightDiscs;
    public Button btnConcede, btnRestartGame, btnQuit;
    public Board board;
    public AvailableMove availableMove;

    private char currentTurn;
    private int darkDiscs, lightDiscs;

    private bool firstTurn;

    void Start()
    {
        btnRestartGame.onClick.AddListener(RestartGame);
        btnConcede.onClick.AddListener(ConcedeGame);
        btnQuit.onClick.AddListener(QuitGame);

        RestartGame();
    }

    private void RestartGame() {
        firstTurn = true;

        DestroyObjectsWithTag("DarkDisc");
        DestroyObjectsWithTag("LightDisc");

        board.SetState(new char[,] {{' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
                                    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
                                    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
                                    {' ', ' ', ' ', 'W', 'B', ' ', ' ', ' '},
                                    {' ', ' ', ' ', 'B', 'W', ' ', ' ', ' '},
                                    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
                                    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
                                    {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}});

        btnConcede.gameObject.SetActive(true);
        btnRestartGame.gameObject.SetActive(false);

        NewTurn();
    }

    public void MakeMove(int x, int y) {
        DestroyObjectsWithTag("AvailableMove");

        board.PlaceDisc(x, y, currentTurn);
        board.FlipDiscs(x, y, currentTurn);

        Invoke("NewTurn", 0.75f);
    }

    private void NewTurn() {
        this.darkDiscs = board.GetDiscs('B').Count;
        this.lightDiscs = board.GetDiscs('W').Count;

        txtDarkDiscs.text = darkDiscs + "";
        txtLightDiscs.text = lightDiscs + "";

        if (firstTurn || currentTurn == 'W') {
            currentTurn = 'B';
            txtCurrentTurn.text = "Black's Turn";
        } else {
            currentTurn = 'W';
            txtCurrentTurn.text = "White's Turn";
        }

        List<Tile> moves = board.GetMoves(currentTurn);

        if(moves.Count != 0) 
        {
            foreach(Tile move in board.GetMoves(currentTurn)) {
                AvailableMove a = Instantiate(this.availableMove);
                a.setPos(move.x, move.y);
                a.colour = currentTurn;
            }
        } 
        else 
        {
            EndGame(this.darkDiscs > this.lightDiscs ? 'B' : 'W');
        }

        firstTurn = false;
    }

    private void ConcedeGame() {
        EndGame(currentTurn == 'B' ? 'W' : 'B');
    }

    private void EndGame(char winner) {
        DestroyObjectsWithTag("AvailableMove");

        if(winner == 'B') {
            txtCurrentTurn.text = "Black Wins";
        } else {
            txtCurrentTurn.text = "White Wins";
        }

        btnConcede.gameObject.SetActive(false);
        btnRestartGame.gameObject.SetActive(true);
    }

    private void QuitGame() {
        Application.Quit();
    }

    private void DestroyObjectsWithTag(string tag) {
        GameObject[] moves = GameObject.FindGameObjectsWithTag(tag);
        foreach(GameObject obj in moves)
        {
            Destroy(obj);
        }
    }
}
