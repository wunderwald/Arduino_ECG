const sum = arr => arr.reduce((total, el) => total + el, 0);
const mean = arr => sum(arr) / arr.length;
const median = arr => [...[...arr].sort()][Math.floor(arr.length / 2)];

const calculateStats = arr => ({
    mean: mean(arr),
    median: median(arr),
    min: Math.min(...arr),
    max: Math.max(...arr)
});

module.exports = { calculateStats, mean, median };