const fs = require('fs');

module.exports = ({time, ecg, finger, fro, arduino}, outputDir, filename) => {
    const numRecords = time.length;
    const head = `time, adi_ecg, adi_finger, adi_fro, ard_fro\n`;
    let body = "";
    for(let i=0; i<numRecords; ++i){
        body = `${body}${time[i]}, ${ecg[i]}, ${finger[i]}, ${fro[i]}, ${arduino[i]}\n`;
    }
    const csv = `${head}${body}`;
    const outputPath = `${outputDir}/${filename}`;
    fs.writeFileSync(outputPath, csv);
}