# Java | Brute Force + Bit Count | O(1) enumerate all times

## Intuition
There are only 12 * 60 = 720 possible times. Simply enumerate all and check if the total bit count of hours + minutes equals `turnedOn`.

## Approach
1. Loop through all hours (0-11) and minutes (0-59).
2. If `Integer.bitCount(h) + Integer.bitCount(m) == turnedOn`, add the formatted time.
3. Return the result list.

## Complexity
- **Time complexity:** O(1) — fixed 720 iterations
- **Space complexity:** O(1) — output size is bounded

## Code
```java
class Solution {
    public List<String> readBinaryWatch(int turnedOn) {
        List<String> result = new ArrayList<>();
        for (int h = 0; h <= 11; h++) {
            for (int m = 0; m <= 59; m++) {
                if (Integer.bitCount(h) + Integer.bitCount(m) == turnedOn) {
                    result.add(h + ":" + (m < 10 ? "0" + m : m));
                }
            }
        }
        return result;
    }
}
```
