import threading
import numpy as np
from scipy.interpolate import interp1d

def resample(ecgSignal, outputSamplingRate_hz):

    # Extract the 'ecg', 'isPeak', 'millis' values from the original data
    ecg = np.array([sample['ecgLevel'] for sample in ecgSignal])
    isPeak = np.array([sample['peakDetected'] for sample in ecgSignal])
    millis = np.array([sample['millis'] for sample in ecgSignal])

    # Calculate the original sampling rate
    inputSamplingRate = 1000 / np.mean(np.diff(millis))

    # Calculate the new time vector based on the desired sampling rate of 1000 Hz
    newTime = np.linspace(millis[0], millis[-1], int((millis[-1] - millis[0]) * outputSamplingRate_hz / inputSamplingRate) + 1)

    # Interpolate 'ecg' and 'millis' using cubic interpolation
    ecgInterpolated = interp1d(millis, ecg, kind='cubic')(newTime)
    millisInterpolated = interp1d(millis, millis, kind='cubic')(newTime)

    # Resample 'isPeak' values by mapping them to the new time vector
    isPeakResampled = np.interp(newTime, millis, isPeak, left=False, right=False).astype(bool)

    # Create the resampled ECG data
    ecgResampled = []
    for ecg, is_peak, millis in zip(ecgInterpolated, isPeakResampled, millisInterpolated):
        ecgResampled.append({
            'ecg': ecg,
            'isPeak': bool(is_peak),
            'millis': int(millis),
        })

    return ecgResampled

def isolatePeaks(peaks):
    out = []
    peakOn = False
    for peak in peaks:
        out.append(peak and not peakOn)
        peakOn = peak
    return out



def parseInput(inputString):
    inputParts = inputString.split(',')
    parsed = {
        'peak': 0,
        'ecg': -1,
        'millis': -1,
    }
    if(inputParts[0] and inputParts[0] != ''):
        parsed['peak'] = inputParts[0]
    if(inputParts[1] and inputParts[1] != ''):
        parsed['ecg'] = inputParts[1]
    if(inputParts[2] and inputParts[2] != ''):
        parsed['millis'] = inputParts[2]
    return parsed


def sampleECG(ard):
    try:
        inputRaw = ard.readline()
        inputDecoded = inputRaw.decode(
            'utf-8').replace('\r', '').replace('\n', '')
        if inputDecoded == '':
            return None
        inputParsed = parseInput(inputDecoded)
        peakDetected = bool(int(inputParsed['peak']))
        ecgLevel = int(inputParsed['ecg'])
        millis = int(inputParsed['millis'])
        return {
            'peakDetected': peakDetected,
            'ecgLevel': ecgLevel,
            'millis': millis,
        }
    except:
        print("! unexpected error while sampling ECG")
        return None


def monitorECG(ard, ecgSignal):
    ecgSample = sampleECG(ard)
    if not ecgSample:
        return
    ecgSignal.append(ecgSample)


class EcgMonitorThread(threading.Thread):
    def __init__(self, ard):
        super().__init__()
        self.stop_flag = threading.Event()
        self.ard = ard
        self.ecgSignal = []

    def run(self):
        while not self.stop_flag.is_set():
            monitorECG(ard=self.ard, ecgSignal=self.ecgSignal)
            pass

    def extractSignalAtEnd(self, length_s):
        if len(self.ecgSignal) <= 0:
            return []
        # get millis of last element
        millisEnd = self.ecgSignal[-1]['millis']
        # filter samples that are in length_s from last sample
        signalFiltered = [sample for sample in self.ecgSignal if sample['millis'] >= (millisEnd - 1000*length_s)]
        return signalFiltered

    def getSignalAndPeaks(self, length_s, samplingRate_hz):
        # extract the last 5 seconds of the recording
        signalExtracted = self.extractSignalAtEnd(length_s=length_s)
        # resample to fixed sampling rate
        signalResampled = resample(ecgSignal=signalExtracted, outputSamplingRate_hz=samplingRate_hz)
        # make output signal
        outputLength = length_s * samplingRate_hz
        numLeadingZeros = max(0, outputLength-len(signalResampled))
        signal = [0 for i in range(numLeadingZeros)]
        peaks = [False for i in range(numLeadingZeros)]
        millis = [0 for i in range(numLeadingZeros)]
        for sample in signalResampled[-outputLength :]:
            signal.append(sample['ecg'])
            peaks.append(sample['isPeak'])
            millis.append(sample['millis'])

        peaks = isolatePeaks(peaks)

        return signal, peaks, millis

    def stop(self):
        self.stop_flag.set()
        super().join()
