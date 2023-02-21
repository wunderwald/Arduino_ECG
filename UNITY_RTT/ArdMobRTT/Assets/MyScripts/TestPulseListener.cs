using UnityEngine;

public class TestPulseListener : MonoBehaviour
{
    void OnMessageArrived(string msg)
    {
        Debug.Log("Msg: " + msg);
    }
}
