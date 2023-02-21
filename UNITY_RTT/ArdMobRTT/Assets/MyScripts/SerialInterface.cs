using UnityEngine;

public class SerialInterface : MonoBehaviour
{

    public GameObject serialControllerPulseReceiver;
    private SerialController _serialControllerPulseReceiver;
    private string currentPulse = "0";

    // messages from SerialControllerPulseSender (= the ecg)
    void OnMessageArrived(string msg)
    {
        currentPulse = msg;
    }
    void OnConnectionEvent(bool success)
    {
        if (success)
            Debug.Log("Sender connected.");
        else
            Debug.Log("Error while connecting sender.");
    }

    void Start()
    {
        _serialControllerPulseReceiver = serialControllerPulseReceiver.GetComponent<SerialController>();
    }

    void Update()
    {
        // Send data
        _serialControllerPulseReceiver.SendSerialMessage(currentPulse);
    }
}
