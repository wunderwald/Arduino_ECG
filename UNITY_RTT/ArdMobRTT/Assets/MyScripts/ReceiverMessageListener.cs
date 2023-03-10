using UnityEngine;

public class ReceiverMessageListener : MonoBehaviour
{
    void OnMessageArrived(string msg)
    {
        return;
    }
    void OnConnectionEvent(bool success)
    {
        if (success)
            Debug.Log("Receiver connected.");
        else
            Debug.Log("Error while connecting receiver.");
    }
}
