/*
by Moritz Wunderwald, 2023
https://github.com/wunderwald/
*/


module.exports = samples => samples.reduce((out, sample) => {
    Object.keys(sample).forEach(key => {
        if(!out[key]){
            out[key] = [];
        }
        out[key].push(sample[key]);
    })
    return out;
}, ({}));