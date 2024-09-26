"use strict";
// you can write to stdout for debugging purposes, e.g.
// console.log('this is a debug message');
Object.defineProperty(exports, "__esModule", { value: true });
function solution(A) {
    // Implement your solution here
    var n = A.length;
    var arr = new Array(n + 1);
    for (var i = 0; i < n; i++) {
        arr[i] = false;
    }
    for (var i = 0; i < n; i++) {
        var val = A[i];
        if (val > 0) {
            arr[val - 1] = true;
        }
    }
    for (var i = 0; i < n; i++) {
        if (arr[i] == false) {
            return i + 1;
        }
    }
    return n + 1;
}
exports.default = solution;
