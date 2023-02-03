# ADI LABCHART DATA PROCESSING

This package converts adi data to input data for www.ibxx.at/validation using frameData and trialData from the matlab scripts.

## Labchart Data Format

The labchart data must have exactly 4 channels. If the changed names are changed from the default settings, please use "ecg", "resp", "fro" and "matlab".

## Input Data Structure

- The .txt files exported from labchart are placed (directly) in ./data/labchart.

- The frameData and trialData files from matlab are placed in ./data/matlab using a single folder for each subject and experiment. The folder name must be the same subjectCode that is used for the labchart files (e.g. "028_ibreath").

## Run the package

The main script of this package is ./main.js. It must be executed using node.js.

- First, [Install node.js](https://nodejs.org/en/)
- Open a Terminal (Mac) or PowerShell (Windows) in the folder of this package
- Type "node main" and hit the return key to process the data
- The processed data is then written to ./data/output. If errors or warnings occur, they are written to the file ./warnings.json.
