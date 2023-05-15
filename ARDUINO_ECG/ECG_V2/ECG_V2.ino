/* ----- TODO -----
- Min IBI: 400ms [variable] (ignore peaks in that peroiod)
----- END TODO ----- */

// ----- Settings -----
// pin numbers
const int TONE_PIN = 2;
const int HEART_PIN = A1;
const int DIGITAL_OUT_PIN = 31;

// live data output settings
const bool SERIAL_OUT = true;         // write data to serial/usb on each loop iteration
const bool SERIAL_OUT_ONLY_PEAK = false; // ignore time and ecg when using serial out
const bool INTERNALS_TO_SERIAL = false; // write filtered signals and adaptive thresh to serial
const bool DIGITAL_OUT = true;         // write peaks to digital output pin
const bool USE_HIGH_WINDOW = true;
const int HIGH_WINDOW = 10; // period of time that output stays high after changing from 0 to 1

// Piezo sound settings
bool PLAY_SOUND = false; /* You can define if you want to activate (true) or deactivate (false) your soundbuzzer. */
int SOUND_FREQ = 1000;   // The frequency of the sound
int SOUND_DURATION = 20; // The duration of the sound in millisconds
// ----- End Settings -----

// ----- Libraries -----
// If you get a compiler error here, you do not have this library. Go to "Tools" --> "Manage libraries" and copy the library name in the field on the top and install it.
#include <ResponsiveAnalogRead.h>
#include <SPI.h>
#include <SD.h>
#include <Adafruit_GFX.h>
// ----- End Libraries -----

// ----- Constants -----
#define HP_CONSTANT ((float)1 / (float)M)
#define RAND_RESOLUTION 100000000
// ----- End Constants -----

// ----- Pan-Tompkins Algorithm Parameters -----
#define M 5         // Here you can change the size for the Highpass filter
#define N 30        // Here you can change the size for the Lowpass filter
#define winSize 250 // this value defines the windowsize which effects the sensitivity of the QRS-detection. May need adjustments depending on your sample size. If you use a lower sampling rate, a lower windowSize might yield  better results.
// ----- End Pan-Tompkins Algorithm Parameters -----

// ----- Pan-Tompkins algorithm -----
// adapted from https://github.com/blakeMilner/real_time_QRS_detection

// circular buffer for input ecg signal
// we need to keep a history of M + 1 samples for HP filter
float ecgBuffer[M + 1] = {0};
int ecgBufferIndex_write = 0;
int ecgBufferIndex_read = 0;

// circular buffer for input ecg signal
// we need to keep a history of N+1 samples for LP filter
float hpfBuffer[N + 1] = {0};
int hpfBufferIndex_write = 0;
int hpfBufferIndex_read = 0;

// LP filter outputs a single point for every input point
// This goes straight to adaptive filtering for evaluation
float ecgSampleFiltered = 0;

// running sums for HP and LP filters, values shifted in FILO
float hpfSum = 0;
float lpfSum = 0;

// variables for adaptive thresholding
float adaptiveThreshold = 0;
bool qrsTriggered = false;
int qrsTriggeredLoopCounter = 0;
float maxSampleInWindow = 0;
int indexInWindow = 0;

// number of starting iterations, used determine when moving windows are filled
int numIterationsInWindow = 0;

// qrs trigger
bool qrsDetected = false;

// detection algorithm
bool detectQRS(float currentEcgSample)
{
  // copy new point into circular buffer, increment index
  ecgBuffer[ecgBufferIndex_write++] = currentEcgSample;
  ecgBufferIndex_write %= (M + 1);

  // temp variable
  int ecgBufferIndex_tmp = 0;

  // High pass filtering (HPF)
  if (numIterationsInWindow < M)
  {
    // first fill buffer with enough points for HP filter
    hpfSum += ecgBuffer[ecgBufferIndex_read];
    hpfBuffer[hpfBufferIndex_write] = 0;
  }
  else
  {
    hpfSum += ecgBuffer[ecgBufferIndex_read];

    ecgBufferIndex_tmp = ecgBufferIndex_read - M;
    if (ecgBufferIndex_tmp < 0)
      ecgBufferIndex_tmp += M + 1;

    hpfSum -= ecgBuffer[ecgBufferIndex_tmp];

    float y1 = 0;
    float y2 = 0;

    ecgBufferIndex_tmp = (ecgBufferIndex_read - ((M + 1) / 2));
    if (ecgBufferIndex_tmp < 0)
      ecgBufferIndex_tmp += M + 1;

    y2 = ecgBuffer[ecgBufferIndex_tmp];

    y1 = HP_CONSTANT * hpfSum;

    hpfBuffer[hpfBufferIndex_write] = y2 - y1;
  }

  // done reading ECG buffer, increment position
  ecgBufferIndex_read++;
  ecgBufferIndex_read %= (M + 1);

  // done writing to HP buffer, increment position
  hpfBufferIndex_write++;
  hpfBufferIndex_write %= (N + 1);

  // Low pass filtering (LPF)
  // shift in new sample from high pass filter
  lpfSum += hpfBuffer[hpfBufferIndex_read] * hpfBuffer[hpfBufferIndex_read];

  if (numIterationsInWindow < N)
  {
    // first fill buffer with enough points for LP filter
    ecgSampleFiltered = 0;
  }
  else
  {
    // shift out oldest data point
    ecgBufferIndex_tmp = hpfBufferIndex_read - N;
    if (ecgBufferIndex_tmp < 0)
    {
      ecgBufferIndex_tmp += (N + 1);
    }
    lpfSum -= hpfBuffer[ecgBufferIndex_tmp] * hpfBuffer[ecgBufferIndex_tmp];

    ecgSampleFiltered = lpfSum;
  }

  // done reading HP buffer, increment position
  hpfBufferIndex_read++;
  hpfBufferIndex_read %= (N + 1);

  // Adapative thresholding for beat detection
  // set initial threshold
  if (numIterationsInWindow < winSize)
  {
    if (ecgSampleFiltered > adaptiveThreshold)
    {
      adaptiveThreshold = ecgSampleFiltered;
    }
    numIterationsInWindow++;
  }

  // check if detection hold off period has passed
  if (qrsTriggered == true)
  {
    qrsTriggeredLoopCounter++;
    if (qrsTriggeredLoopCounter >= 100)
    {
      qrsTriggered = false;
      qrsTriggeredLoopCounter = 0;
    }
  }

  // find if we have a new max
  if (ecgSampleFiltered > maxSampleInWindow)
    maxSampleInWindow = ecgSampleFiltered;

  // find if we are above adaptive threshold: if yes, peak has been detected
  if (ecgSampleFiltered > adaptiveThreshold && !qrsTriggered)
  {
    qrsTriggered = true;
    return true;
  }

  // adjust adaptive threshold using max of sample in previous window
  if (indexInWindow++ >= winSize)
  {
    // weighting factor for determining the contribution of
    // the current peak value to the threshold adjustment
    float gamma = 0.4;

    // forgetting factor: rate at which we forget old observations
    // choose a random value between 0.01 and 0.1 for this,
    float alpha = 0.1 + (((float)random(0, RAND_RESOLUTION) / (float)(RAND_RESOLUTION)) * ((0.1 - 0.01)));

    // compute new threshold
    adaptiveThreshold = alpha * gamma * maxSampleInWindow + (1 - alpha) * adaptiveThreshold;

    // reset current window index
    indexInWindow = 0;
    maxSampleInWindow = -10000000;
  }

  // return false if we didn't detect a new QRS
  return false;
}
// ----- End Pan-Tompkins algorithm -----

// ----- Initialization -----
// enable responsive analog read on the ECG pin
ResponsiveAnalogRead analog(HEART_PIN, true);

// calculation of time between QRS interval
int timeCprRead1_millis = 0;
int timeCprRead2_millis = 0;
int timeCPR = 0;
float cprInterval_millis;
int currentEcgSample;

// timing of peaks
unsigned long timeCurrentPeak_micros = 0; // time at which last QRS was found
unsigned long timePreviousPeak = 0;       // time at which QRS before last was found
unsigned long currentMicros = 0;          // current time
unsigned long timeRRPeak_millis = 0;

// loop timing
float lastLoopDuration_millis = 0;

// sound timing
unsigned long timeLastSoundStart_millis = 0;

// data output counters
int highWindowCounter = 0;
// ----- End Initialization -----

// ----- Setup -----
void setup()
{
  Serial.begin(115200);
  if (DIGITAL_OUT)
  {
    pinMode(DIGITAL_OUT_PIN, OUTPUT);
  }
}
// ----- End Setup -----

// ----- Loop -----
void loop()
{
  delay(2);

  // update time
  currentMicros = micros();

  // update ecg sample
  int currentEcgSample = analogRead(HEART_PIN);

  // Write data to serial: <peak>,<ecg>,<time>
  if (SERIAL_OUT)
  {
    Serial.print(int(qrsDetected));
    if(!SERIAL_OUT_ONLY_PEAK)
    {
      Serial.print(",");
      Serial.print(currentEcgSample);
      Serial.print(",");
      Serial.print(millis());
    }
    Serial.println();
  }

  // write internal signals to serial (for testing)
  if (INTERNALS_TO_SERIAL)
  {
    Serial.print(ecgSampleFiltered);
    Serial.print(",");
    Serial.print(adaptiveThreshold);
    Serial.println();
  }

  // write to digital output pin
  if (DIGITAL_OUT)
  {
    // write output using windowed method (stay high for a couple of loops after qrs has been detected)
    if (USE_HIGH_WINDOW)
    {
      // update high window
      if (qrsDetected)
      {
        highWindowCounter = HIGH_WINDOW;
      }
      else if (highWindowCounter > 0)
      {
        highWindowCounter -= 1;
      }
      digitalWrite(DIGITAL_OUT_PIN, highWindowCounter > 0);
    }
    // write qrs without window method (write peak only in a single loop)
    else
    {
      digitalWrite(DIGITAL_OUT_PIN, qrsDetected ? HIGH : LOW);
    }
  }

  // update peak detection algorithm
  qrsDetected = detectQRS(currentEcgSample);
  if (qrsDetected)
  {
    timeCurrentPeak_micros = micros();
    timeRRPeak_millis = millis();
    timeCprRead2_millis = timeCprRead1_millis;
    timeCprRead1_millis = millis();
    cprInterval_millis = timeCprRead1_millis - timeCprRead2_millis;
  }

  // play a sound if peak is detected (during multiple loop iterations)
  if (lastLoopDuration_millis > cprInterval_millis && PLAY_SOUND == true)
  {
    tone(TONE_PIN, SOUND_FREQ, SOUND_DURATION);
    timeLastSoundStart_millis = millis();
  }
  lastLoopDuration_millis = millis() - timeLastSoundStart_millis;
}
// ----- End Loop -----
