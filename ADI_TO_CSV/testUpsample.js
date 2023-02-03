const upsample = require("./upsampleStep");

const src = [1, 2, 3, 4];
const destLengthEven = 16;
const destLengthOdd = 21;

console.log(upsample(src, destLengthEven));
console.log(upsample(src, destLengthOdd));