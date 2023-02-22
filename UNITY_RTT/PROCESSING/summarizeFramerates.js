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

export const summarizeFrameRates = () => {

    // get input files
    const INPUT_DIR = './data';
    const inputFiles = fs.readdirSync(INPUT_DIR)
        .filter(f => f.includes('framerate_log'))
        .filter(f => f.endsWith('.csv'))
        .map(f => ({
            name: f.replace('.csv', ''),
            path: `${INPUT_DIR}/${f}`
        }));

    log(`discovered ${inputFiles.length} input files:\n${inputFiles.map(f => `    - ${f.name}\n`).join('')}`)

    // initialize output data
    const allFramerates = [];

    // process files
    for(const {name, path} of inputFiles){
        log(`processing ${name}`);

        //parse
        const rawData = fs.readFileSync(path);
        const data = parse(rawData, {columns: true});

        data.forEach(record => allFramerates.push(+record['Frame Rate']));
    }


    // calculate summary stats
    const summary = sumaryStats(allFramerates);

    // log output
    LOG && console.log();
    log('Summary of frame rates:')
    LOG && console.log(summary);

    // write output to file
    fs.writeFileSync('./frameRateSummary.json', JSON.stringify(summary));
    
};
