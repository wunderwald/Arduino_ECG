# UNITY RTT

This package contains a Unity project that is used in the process of estimating latencies between peak detection on the Arduino ECG and registration in a Unity application. Latencies are estimated as `latency = 1/2 * rtt` where `rtt` is the round-trip-time between Arduino and Unity. Whenever a peak is registered in Unity, a signal is sent back to Arduino so that the delay time between arduino and unity (rtt) can be measured. It uses the library [Ardity](https://github.com/dwilches/Ardity) to enable asynchronous serial communication.

## Hardware
- Arduino ECG (sender)
- Second Arduino for receiving data from Unity (receiver)
- AD Instruments PowerLab
- AD Instruments LabRecorder
- Unity and Ardity

## Usage

* In LabRecorder, record two channels: 
1. Direct output from Arduino ECG
2. Output of second Arduino 
* Arduino ECG sends peak data in two ways:
1. to ADI via analog output pin
2. to Unity through serial communication
* When a peak is registered in Unity, it sends a trigger to the second Arduino.
* The second Arduino uses an analog output pin to forward it to ADI / LabRecorder

## Code

- Arduino code for the receiver is in `./Arduino/ArdMob_RTT_PulseReceiver`
- The Unity code is in `./ArdMobRTT`
- The Code for the Arduino ECG is in `../ARDUINO_ECG/ECG`

## Author

This package has been written by Moritz Wunderwald ([github 🧑‍💻](https://github.com/wunderwald))