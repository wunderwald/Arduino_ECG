import threading

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
        inputDecoded = inputRaw.decode('utf-8').replace('\r', '').replace('\n', '')
        if inputDecoded == '':
            return None
        inputParsed = parseInput(inputDecoded);
        peakDetected = bool(int(inputParsed['peak']))
        ecgLevel = int(inputParsed['ecg'])
        return {
            'peakDetected': peakDetected,
            'ecgLevel': ecgLevel
        }
    except:
        print("! unexpected error while sampling ECG")
        return None
    
def monitorECG(ard, peakQueue, ecgSignal):
    ecgData = sampleECG(ard)
    if ecgData['peakDetected']:   
        peakQueue.put(True)
    ecgSignal.append({'millis': ecgData['millis'], 'ecgLevel': ecgData['ecgLevel']})


class EcgMonitorThread(threading.Thread):
    def __init__(self, ard, peakQueue, ecgSignal):
        super().__init__()
        self.stop_flag = threading.Event()
        self.ard = ard
        self.peakQueue = peakQueue
        self.ecgSignal = ecgSignal

    def run(self):
        while not self.stop_flag.is_set():
            monitorECG(ard=self.ard, peakQueue=self.peakQueue, ecgSignal=self.ecgSignal)
            pass

    def stop(self):
        self.stop_flag.set()
        super().join()