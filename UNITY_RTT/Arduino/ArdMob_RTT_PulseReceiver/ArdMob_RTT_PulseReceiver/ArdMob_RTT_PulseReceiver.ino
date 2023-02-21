/*
  ## ArdMobRTT Pulse Receiver ##

  reads messages from serial bus: '0' (no pulse) or '1' (pulse)
  this data is the written to digital output
*/

int PULSE_OUT_PIN = 13;
bool LOG = false;

void log(int val)
{ 
  if(!LOG) return;
  Serial.println(val);
}

void setup()
{
    Serial.begin(115200);
    pinMode(PULSE_OUT_PIN, OUTPUT);
    digitalWrite(PULSE_OUT_PIN, LOW);
}

void loop()
{
    switch (Serial.read())
    {
        case '0':
            log(0);
            digitalWrite(PULSE_OUT_PIN, LOW);
            break;
        case '1':
            log(1);
            digitalWrite(PULSE_OUT_PIN, HIGH);
            break;
    }
}