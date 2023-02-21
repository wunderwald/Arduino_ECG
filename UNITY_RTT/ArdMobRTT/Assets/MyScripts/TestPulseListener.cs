/*
by Moritz Wunderwald, 2023
https://github.com/wunderwald/
moritzwunderwald@yahoo.de
*/

using UnityEngine;

public class TestPulseListener : MonoBehaviour
{
    void OnMessageArrived(string msg)
    {
        Debug.Log("Msg: " + msg);
    }
}
