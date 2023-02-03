const writeJSON = require('../iBXX/writeJSON');
const fs = require('fs');

const mkdirIfNotExists = dir => {
    if(!fs.existsSync(dir)){
        fs.mkdirSync(dir);
    }
}

module.exports = (trial, subjectId, outputDir) => {
    //directory for file
    const subjectDir = `${outputDir}/subject_${subjectId}`;
    mkdirIfNotExists(subjectDir);

    //write file for trial
    const trialPath = `${subjectDir}/trial_${trial.trialIndex}.json`;
    writeJSON(trial, trialPath);
}