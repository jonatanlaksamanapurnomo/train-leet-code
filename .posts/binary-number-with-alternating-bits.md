# Java | Bit Manipulation | O(log n) XOR adjacent bits

## Intuition
Compare each bit with its neighbor using right-shift and XOR. If any adjacent pair is the same, XOR yields 0 instead of 1.

## Approach
1. Right-shift `n` by 1 to get the "alternate" version.
2. Compare the last bit of both using XOR — it must be 1 for alternating bits.
3. Shift both right and repeat until done.

## Complexity
- **Time complexity:** O(log n)
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public boolean hasAlternatingBits(int n) {
        int alternate = (n >> 1);
        while (alternate > 0) {
            int lastAlternateBit = alternate & 1;
            int lastNBit = n & 1;
            int bit = lastAlternateBit ^ lastNBit;
            if (bit != 1) return false;
            alternate >>= 1;
            n >>= 1;
        }
        return true;
    }
}
```
