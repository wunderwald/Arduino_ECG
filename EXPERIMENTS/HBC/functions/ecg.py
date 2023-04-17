
    
import threading

def sampleECG(ard):
    try:
        inputRaw = ard.readline()
        inputParsed = inputRaw.decode('utf-8').replace('\r', '').replace('\n', '')
        if inputParsed == '':
            return None
        peakDetected = bool(int(inputParsed))
        return peakDetected
    except:
        print("! unexpected error while sampling ECG")
        return None
    
def monitorECG(ard, peakQueue):
    peakDetected = sampleECG(ard)
    if peakDetected:   
        peakQueue.put(True)


class EcgMonitorThread(threading.Thread):
    def __init__(self, ard, peakQueue):
        super().__init__()
        self.stop_flag = threading.Event()
        self.ard = ard
        self.peakQueue = peakQueue

    def run(self):
        while not self.stop_flag.is_set():
            monitorECG(ard=self.ard, peakQueue=self.peakQueue)
            pass

    def stop(self):
        self.stop_flag.set()
        super().join()