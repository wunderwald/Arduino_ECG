const writeJSON = require('./writeJSON');

module.exports = warnings => {
    writeJSON(warnings, './warnings.json');
}