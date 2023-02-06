import * as fs from 'fs';
import { parse } from 'csv-parse/sync';

// logger
const LOG = true;
const log = msg => LOG && console.log(`# ${msg}`);

// get input files
const INPUT_DIR = '../ADI_TO_CSV/data/output';
const inputFiles = fs.readdirSync(INPUT_DIR)
    .filter(f => f.endsWith('.csv'))
    .map(f => ({
        name: f.replace('.csv', ''),
        path: `${INPUT_DIR}/${f}`
    }));

log(`discovered ${inputFiles.length} input files:\n${inputFiles.map(f => `    - ${f.name}\n`).join('')}`)

// initialize output containers
const timingData = {
    peaksAdi: [],
    peaksArd: [],
    peakPairs: [],
    deltaTimes: [],
    meanDeltaTime: null,
    medianDeltaTime: null,
    missedPeaksArd: null,
};

// process files
const isHigh = val => val > 4;
for(const {name, path} of inputFiles){
    log(`processing ${name}`);
    
    //parse
    const rawData = fs.readFileSync(path);
    const channelNames = []
    const data = parse(rawData, {columns: true});

    // get peak indices
    for(let i=1; i<data.length; ++i) {
        const lastSample = data[i-1];
        const sample = data[i];
        if(!isHigh(lastSample.adi_fro) && isHigh(sample.adi_fro)){
            timingData.peaksAdi.push({
                index: i,
                time: sample.time,
            });
        }
        if(!isHigh(lastSample.ard_fro) && isHigh(sample.ard_fro)){
            timingData.peaksArd.push({
                index: i,
                time: sample.time,
                marked: false
            });
        }
    }

    // match peaks: find ard peak for each adi peak
    for(const adiPeak of timingData.peaksAdi){

    }

    // determine number of peaks that have been missed / not detected

    // filter peaks: remove the K longest delta times for K = abs(len(adiPeaks - ardPeaks))

    // calculate delta times

    // calculate summary stats

    // export data
}

