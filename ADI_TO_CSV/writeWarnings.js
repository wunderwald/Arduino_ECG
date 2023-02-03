const writeJSON = require('../iBXX/writeJSON');

module.exports = warnings => {
    writeJSON(warnings, './warnings.json');
}