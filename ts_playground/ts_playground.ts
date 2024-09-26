// you can write to stdout for debugging purposes, e.g.
// console.log('this is a debug message');

function solution(A: number[]): number {
    // Implement your solution here
    let n: number = A.length
    let arr: boolean[] = new Array(n + 1)
    for (let i = 0; i<n; i++) {
        arr[i] = false
    }
    for (let i = 0; i<n; i++) {
        let val: number = A[i]
        if (val > 0) {
            arr[val - 1] = true
        }
    }
    for (let i =0; i<n; i++) {
        if (arr[i] == false) {
            return i + 1
        }
    }
    return n + 1
}

export default solution