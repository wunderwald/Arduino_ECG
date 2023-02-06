# By Moritz Wunderwald, 2022

import os
import neurokit2 as nk
import pandas as pd
import json

inputDir = '../ADI_TO_CSV/data/output'
outputDirDashboardInput = './dashboardInputData'
outputDirDashboardInputFinger = './dashboardInputDataFinger'
outputDirProcessedData = './processedData'
samplingRateLabchart = 1000

# get list of input files
inputFiles = [ file for file in os.listdir(inputDir) if ".csv" in file]

# process files
for inputFile in inputFiles:
    print(f"# Processing {inputFile}")

    # read file
    inputPath = f"{inputDir}/{inputFile}"
    inputData = pd.read_csv(inputPath)
    ecgSignal = inputData['adi_ecg']
    fingerSignal = inputData['adi_finger']

    # detect peaks in ecg and finger signal
    ecgSignals, ecgInfo = nk.ecg_process(ecgSignal, sampling_rate=samplingRateLabchart)
    rPeaks = ecgInfo["ECG_R_Peaks"]
    ecgSignalCleaned = ecgSignals["ECG_Clean"]
    fingerSignals, fingerInfo = nk.ecg_process(ecgSignal, sampling_rate=samplingRateLabchart)
    fingerRPeaks = fingerInfo["ECG_R_Peaks"]
    fingerSignalCleaned = fingerSignals["ECG_Clean"]

    # collect dashboardInputData
    dashboardInputData = {
        'ecg': [{'index': i, 'ecg': ecg} for ecg, i in enumerate(ecgSignalCleaned)],
        'peaks': rPeaks.tolist(),
        'startIndex': 0,
        'endIndex': len(ecgSignalCleaned),
        'removedRegions': [],
        'samplingRate': samplingRateLabchart
    }

    # write dashboard input data to file
    outputPathDashboardInput = f"{outputDirDashboardInput}/{inputFile.replace('.csv', '.json')}"
    print(f"... Writing dashboard input data to {outputPathDashboardInput}.")
    with open(outputPathDashboardInput, "w") as outfile:
        json.dump(dashboardInputData, outfile)  

    # collect dashboardInputData (finger sensor)
    dashboardInputDataFinger = {
        'ecg': [{'index': i, 'ecg': ecg} for ecg, i in enumerate(fingerSignalCleaned)],
        'peaks': fingerRPeaks.tolist(),
        'startIndex': 0,
        'endIndex': len(fingerSignalCleaned),
        'removedRegions': [],
        'samplingRate': samplingRateLabchart
    }

    # write dashboard input data to file (finger sensor)
    outputPathDashboardInputFinger = f"{outputDirDashboardInputFinger}/{inputFile.replace('.csv', '_finger.json')}"
    print(f"... Writing dashboard input data for finger sensor to {outputPathDashboardInputFinger}.")
    with open(outputPathDashboardInputFinger, "w") as outfile:
        json.dump(dashboardInputDataFinger, outfile)  

    # add cleaned signals and peaks to input data
    inputData['adi_ecg_clean_nk2'] = ecgSignalCleaned
    inputData['adi_finger_clean_nk2'] = fingerSignalCleaned
    inputData['adi_ecg_peaks_nk2'] = [5 if index in rPeaks else 0 for index in range(len(ecgSignalCleaned))]
    inputData['adi_finger_peaks_nk2'] = [5 if index in fingerRPeaks else 0 for index in range(len(fingerSignalCleaned))]

    # write processed input data to csv
    outputPathProcessedData = f"{outputDirProcessedData}/{inputFile.replace('.csv', '_nk2.csv')}"
    print(f"... Writing processed data to {outputPathProcessedData}.")
    inputData.to_csv(outputPathProcessedData, index=False)

    print("... done")
