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
    while True:
        peakDetected = sampleECG(ard)
        if peakDetected:
            peakQueue.put(True)