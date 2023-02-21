# PROCESS CSV RECORDINGS

This package reads data from csv files that have been created using `../ADI_TO_CSV` and creates summary statistics about delays between different methods of detecting R-Peaks.

## Usage

1. run `../ADI_TO_CSV/main.js` to vreate ecg `.csv` files from `.txt` files that have been exported from LabChart.
2. run `./main.js`using the command `node main`
3. the resulting data is written to `./summary.json`

## Author

This package has been written by Moritz Wunderwald ([github 🧑‍💻](https://github.com/wunderwald))