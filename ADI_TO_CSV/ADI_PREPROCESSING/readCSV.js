const fs = require('fs');
const parse = require('csv-parse/lib/sync');

module.exports = relPath => {
    const content = fs.readFileSync(relPath, {encoding: "ascii"});
    const data = parse(content, {
        columns: true,
        skip_empty_lines: true,
    });
    return data;
}