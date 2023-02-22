/*
by Moritz Wunderwald, 2023
https://github.com/wunderwald/
moritzwunderwald@yahoo.de
*/

import * as fs from 'fs';
import { parse } from 'csv-parse/sync';
import { sumaryStats, mean } from './stats.js';
 
// logger
const LOG = true;
const log = msg => LOG && console.log(`# ${msg}`);

export const summarizeLatencies = () => {

    // get input files
    const INPUT_DIR = './data';
    const inputFiles = fs.readdirSync(INPUT_DIR)
        .filter(f => f.includes('latency_validation'))
        .filter(f => f.endsWith('.csv'))
        .map(f => ({
            name: f.replace('.csv', ''),
            path: `${INPUT_DIR}/${f}`
        }));

    log(`discovered ${inputFiles.length} input files:\n${inputFiles.map(f => `    - ${f.name}\n`).join('')}`)

    // initialize output data
    const timingDataPerRecording = [];

    // process files
    for(const {name, path} of inputFiles){
        log(`processing ${name}`);

        // initialize timing data
        const timingData = {
            peaksSend: [],
            peaksReturn: [],
            peakPairs: [],
            peakPairsFiltered: [],
            unmatchedSentPeaks: null,
            unmatchedRatio: null,
            deltaTimes_ms: [],
            meanDeltaTime_ms: null,
            medianDeltaTime_ms: null,
            maxDeltaTime_ms: null,
            minDeltaTime_ms: null,
        };
        
        //parse
        const rawData = fs.readFileSync(path);
        const data = parse(rawData, {columns: true});

        // get peak indices
        for(let i=1; i<data.length; ++i) {
            const lastSample = data[i-1];
            const sample = data[i];
            const isHigh = val => val > 4 || isNaN(val);    //isNaN works on peak_return bc of recording (out of range) error
            if(!isHigh(lastSample.peak_send) && isHigh(sample.peak_send)){
                timingData.peaksSend.push({
                    index: i,
                    time_s: sample.time,
                });
            }
            if(!isHigh(lastSample.peak_return) && isHigh(sample.peak_return)){
                timingData.peaksReturn.push({
                    index: i,
                    time_s: sample.time,
                });
            }
        }

        console.log(timingData.peaksSend);
        console.log(timingData.peaksReturn);

        // match peaks: find return peak for each sent peak
        const matchPeak = (peak, peakList) => {
            let minDelta = Number.POSITIVE_INFINITY;
            let closestMatch = null;
            for(const candidate of peakList){
                const delta = Math.abs(candidate.time_s - peak.time_s);
                if(delta < minDelta){
                    closestMatch = candidate;
                    minDelta = delta;
                }
            }
            return closestMatch;
        }
        const largerPeakListId = timingData.peaksSend.length >= timingData.peaksReturn.length ? 'adi' : 'ard';
        const largerPeakList = largerPeakListId === 'adi' ? timingData.peaksSend : timingData.peaksReturn;
        const smallerPeakList = largerPeakListId === 'adi' ? timingData.peaksReturn : timingData.peaksSend;
        for(const peakA of largerPeakList){
            const peakB = matchPeak(peakA, smallerPeakList);
            const peakPair = {
                peakArd: largerPeakListId === 'adi' ? peakB : peakA,
                peakAdi: largerPeakListId === 'adi' ? peakA : peakB,
            }
            peakPair.delta_s = peakPair.peakArd.time_s - peakPair.peakAdi.time_s; 
            
            timingData.peakPairs.push(peakPair);
        }

        // determine number of peaks that have been missed / not detected
        timingData.unmatchedAdiPeaks = timingData.peaksSend.length - timingData.peaksReturn.length;
        const absUnmatchedPeaks = Math.abs(timingData.unmatchedAdiPeaks);
        timingData.unmatchedRatio = absUnmatchedPeaks / largerPeakList.length;

        // filter peaks: 
        // 1.: remove the K longest delta times for K = <numMissedPeaks>
        // 2.: remove outliers: 5% of largest delta times
        const compareAbsDelta = (a, b) => {
            const diff = Math.abs(a.delta_s - b.delta_s);
            if(diff === 0) return 0;
            if(diff < 0) return 1;
            return -1;
        }
        const outlierFilter = pairs => {
            const sorted = [...[...pairs].sort(compareAbsDelta)];
            const quantilePair = sorted[Math.floor(sorted.length * .05)];
            return pairs.filter(pair => Math.abs(pair.delta_s) < Math.abs(quantilePair.delta_s));
        };
        const peakPairsSortedByDelta = [...[...timingData.peakPairs].sort(compareAbsDelta)];
        const peakPairsNoMissedPeaks = [];
        for(let i=absUnmatchedPeaks; i<peakPairsSortedByDelta.length; ++i){
            peakPairsNoMissedPeaks.push(peakPairsSortedByDelta[i]);
        }
        const peakPairsNoOutliers = outlierFilter(peakPairsNoMissedPeaks);
        timingData.peakPairsFiltered = [...peakPairsNoOutliers];

        // calculate delta times
        timingData.deltaTimes_ms = timingData.peakPairsFiltered.map(pair => pair.delta_s * 1000);

        // calculate stats
        const stats = sumaryStats(timingData.deltaTimes_ms);
        timingData.meanDeltaTime_ms = stats.mean;
        timingData.medianDeltaTime_ms = stats.median;
        timingData.minDeltaTime_ms = stats.min;
        timingData.maxDeltaTime_ms = stats.max;

        // push data to collection
        timingDataPerRecording.push(timingData);
    }

    // calculate summary stats
    const allDeltaTimes_ms = timingDataPerRecording.reduce((arr, el) => [...arr, ...el.deltaTimes_ms], []);
    const deltaStats = sumaryStats(allDeltaTimes_ms);
    const allUnmatchedPercentages = timingDataPerRecording.map(el => el.unmatchedRatio);
    const unmatchedStats = sumaryStats(allUnmatchedPercentages);
    const summary = {
        meanDeltaTime_ms: deltaStats.mean.toFixed(4),
        medianDeltaTime_ms: deltaStats.median.toFixed(4),
        minDeltaTime_ms: deltaStats.min.toFixed(4),
        maxDeltaTime_ms: deltaStats.max.toFixed(4),
        meanMinDeltaTime_ms: mean(timingDataPerRecording.map(d => d.minDeltaTime_ms)).toFixed(4),
        meanMaxDeltaTime_ms: mean(timingDataPerRecording.map(d => d.maxDeltaTime_ms)).toFixed(4),
        meanUnmatchedPeaksRatio: unmatchedStats.mean.toFixed(4),
        medianUnmatchedPeaksRatio: unmatchedStats.median.toFixed(4),
        totalNumPeaks: allDeltaTimes_ms.length,
    }

    // log output
    LOG && console.log();
    log('Summary of delta times and unmatched peaks:')
    LOG && console.log(summary);

    // write output to file
    fs.writeFileSync('./latencySummary.json', JSON.stringify(summary));
}
