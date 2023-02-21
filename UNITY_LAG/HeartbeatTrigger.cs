using UnityEngine;

public class HeartbeatTrigger : MonoBehaviour
{
    // output
    public bool heartbeat = false;
    
    // qrs state
    private int lastQRS = 0;
    public int QRS = 0;
    
    // message receiver for serial controller
    void OnMessageArrived(string message)
    {
        QRS = int.Parse(message);
        // update heartbeat
        heartbeat = lastQRS == 0 && QRS == 1;
        lastQRS = QRS;
    }

    void OnConnectionEvent(bool isConnected)
    {
        Debug.Log(isConnected ? "# Arduino connected via Ardity" : "# Arduino disconnected");
    }
}
