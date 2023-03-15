from pathlib import Path
import os

def makeCsvHC(trialData):
    keys = ['subjectId', 'trialIndex', 'duration_s', 'numHeartbeatsTracked', 'numHeartbeatsCounted', 'confidenceRating', 'startTime_s', 'endTime_s']
    head = f"{', '.join(keys)}\n"
    body = ""
    for d in trialData:
        body = f"{body}{', '.join([str(d[key]) for key in keys])}\n"
    return f"{head}{body}"

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