import os
import neurokit2 as nk
import pandas as pd

inputDir = '../ADI_TO_CSV/data/output'
outputDirDashboardInput = './dashboardInputData'
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

    # collect dashoardInputData
    dashoardInputData = {
        'ecg': [{'index': i, 'ecg': ecg} for ecg, i in enumerate(ecgSignalCleaned)],
        'peaks': rPeaks,
        'startIndex': 0,
        'endIndex': len(ecgSignalCleaned),
        'removedRegions': [],
        'samplingRate': samplingRateLabchart
    }

    # add cleaned signals and peaks to input data
    inputData['adi_ecg_clean_nk2'] = ecgSignalCleaned
    inputData['adi_finger_clean_nk2'] = fingerSignalCleaned
    inputData['adi_ecg_peaks_nk2'] = [5 if index in rPeaks else 0 for index in range(len(ecgSignalCleaned))]
    inputData['adi_finger_peaks_nk2'] = [5 if index in fingerRPeaks else 0 for index in range(len(fingerSignalCleaned))]

    # write to files: .json as dashboard input, .csv for further processing
    outputPathDashboardInput = f"{outputDirDashboardInput}/{inputFile.replace('.csv', '.json')}"
    print(f"... Writing dashboard input data to {outputPathDashboardInput}.")

    outputPathProcessedData = f"{outputDirProcessedData}/{inputFile.replace('.csv', '_nk2.csv')}"
    print(f"... Writing processed data to {outputPathProcessedData}.")
    inputData.to_csv(outputPathProcessedData, index=False)

    print("... done")
