# Java | Bit Manipulation | O(1) shift and build reversed integer

## Intuition
Extract the last bit of `n` and append it to the result by shifting result left and OR-ing with the extracted bit. Repeat 32 times.

## Approach
1. Initialize `result = 0`.
2. For each of the 32 bits: left-shift result, OR with `n & 1`, then right-shift `n`.
3. Return result.

## Complexity
- **Time complexity:** O(1) — fixed 32 iterations
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public int reverseBits(int n) {
        int result = 0;
        for (int i = 0; i < 32; i++) {
            result = (result << 1) | (n & 1);
            n >>= 1;
        }
        return result;
    }
}
```
