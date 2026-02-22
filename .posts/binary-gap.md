# Java | Bit Manipulation | O(log n) track last set bit position

## Intuition
Iterate through bits of `n`. Whenever we encounter a set bit, compute the distance from the last set bit and update the maximum gap.

## Approach
1. Track `lastOnePos` and `currentPos` starting at position 1.
2. For each bit: if it's 1 and we've seen a previous 1, update the max gap.
3. Right-shift `n` and increment position until `n` is 0.

## Complexity
- **Time complexity:** O(log n)
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public int binaryGap(int n) {
        int resp = 0;
        int lastOnePos = 0;
        int currentPos = 1;
        while (n > 0) {
            if ((n & 1) == 1) {
                if (lastOnePos > 0) {
                    resp = Integer.max(resp, currentPos - lastOnePos);
                }
                lastOnePos = currentPos;
            }
            n >>= 1;
            currentPos++;
        }
        return resp;
    }
}
```
