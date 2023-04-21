from pathlib import Path
import os

def makeCsv(data, keys):
    head = f"{', '.join(keys)}\n"
    body = ""
    for d in data:
        body = f"{body}{', '.join([str(d[key]) for key in keys])}\n"
    return f"{head}{body}"

def makeSubjectCsv(trialData):
    keys = ['subjectId', 'trialIndex', 'duration_s', 'numHeartbeatsTracked', 'numHeartbeatsCounted', 'confidenceRating', 'startTime_s', 'endTime_s']
    return makeCsv(data=trialData, keys=keys)

def makeEcgCsv(ecgSignal):
    keys = ['millis', 'ecgLevel', 'peakDetected', 'trialStart', 'trialEnd']
    return makeCsv(data=ecgSignal, keys=keys)

def csvToFile(csv, dir, filename):
    # make dirs if necessary
    outputDir = Path(dir)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # create path
    outputPath = Path(outputDir, filename)

    # write
    with open(outputPath, "w") as outputFile:
        outputFile.write(csv)