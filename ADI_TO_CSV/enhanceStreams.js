/*
by Moritz Wunderwald, 2023
https://github.com/wunderwald/
moritzwunderwald@yahoo.de
*/

//alternative to Math.max for big arrays
const max = arr => arr.reduce((currentMax, val) => {
    currentMax = (val > currentMax) ? val : currentMax;
    return currentMax;
}, Number.NEGATIVE_INFINITY);

const invertSignal = signal => signal.map(value => (value * -1));

// mirror fro signal at y axis, then translate it along the x axis by amplitude
const invertFRO = fro => {
    const amp = max(fro);
    const froNorm = fro.map(value => value/amp);
    return invertSignal(froNorm).map(value => value + 1)
}

const makeEcgXFro = (ecg, fro) => {
    if(ecg.length !== fro.length) console.error("FRO and ECG signals must have equal length");
    const inverseFRO = invertFRO(fro);
    return inverseFRO.map((froSample, i) => {
        const ecgSample = ecg[i];
        return froSample * ecgSample;
    })
};

module.exports = streams => {
    const streamTitles = new Set(Object.keys(streams));
    if(streamTitles.has('ecg') && streamTitles.has('fro')){
        streams['ecg_x_fro'] = makeEcgXFro(streams.ecg, streams.fro);
    }
    return streams;
};