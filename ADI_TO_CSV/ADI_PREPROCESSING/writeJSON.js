const fs = require('fs');

module.exports = (json, path) => {
    const o = {data: json};
    const s = JSON.stringify(o);
    fs.writeFileSync(path, s);
}