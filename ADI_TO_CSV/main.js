const discoverInputFiles = require('./discoverInputFiles');
const readRawDataAdi = require('./readRawData');
const flatten = require('./flattenAdiData');

const warn = w => console.warn(`❌ ${w}`);

const main = () => {

    const outputDir = './data/output';
    
    //discover input files
    const rawDir = './data/labchart';
    const rawFiles = discoverInputFiles(rawDir, 'txt');

    console.log(rawFiles);


    rawFiles.forEach((rawFile) => {
        const rawPath = `${rawDir}/${rawFile}`;
        console.log(`\n\n${rawPath}`);

        //read adi data (output array of objects: {recordingIndex, data})
        const recordings = readRawDataAdi(rawPath);

        //select recording to be processed
        const recording = recordings[recordings.length - 1].data;   // TODO: is this correct??

        //flatten data (create 1d stream per channel)
        const streams = flatten(recording);

    });
};

main();