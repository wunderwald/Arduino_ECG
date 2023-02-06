export const sum = arr => arr.reduce((total, el) => total + el, 0);
export const mean = arr => sum(arr) / arr.length;
export const median = arr => [...[...arr].sort()][Math.floor(arr.length / 2)];
export const sumaryStats = arr => ({
    mean: mean(arr),
    median: median(arr),
    min: Math.min(...arr),
    max: Math.max(...arr)
});