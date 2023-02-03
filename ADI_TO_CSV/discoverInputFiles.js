const fs = require('fs');

module.exports = (inputDir, fileType) => fs.readdirSync(inputDir)
    .filter(item => fs.lstatSync(`${inputDir}/${item}`).isFile())
    .filter(file => file.endsWith(fileType));