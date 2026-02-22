# Java | Sliding Window | O(n) using last seen index tracking

## Intuition
For each position, if all three characters (a, b, c) have been seen, the number of valid substrings ending at that position equals the smallest last-seen index + 1.

## Approach
1. Track the last seen index of each character a, b, c (initialized to -1).
2. Iterate through the string, updating the last seen index of the current character.
3. If all three characters have been seen (no -1 in the array), add `min(lastIdx) + 1` to the result.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public int numberOfSubstrings(String s) {
        int[] lastIdx = new int[]{-1, -1, -1};
        int resp = 0;
        for (int i = 0; i < s.length(); i++) {
            int charToIdx = s.charAt(i) - 'a';
            lastIdx[charToIdx] = i;
            if (validCharSet(lastIdx)) {
                int smallestIdx = getSmallestIdx(lastIdx);
                resp += smallestIdx + 1;
            }
        }
        return resp;
    }

    public static boolean validCharSet(int[] lastIdx) {
        for (int i = 0; i < lastIdx.length; i++) {
            if (lastIdx[i] == -1) return false;
        }
        return true;
    }

    public static int getSmallestIdx(int[] lastIdx) {
        int resp = Integer.MAX_VALUE;
        for (int i = 0; i < lastIdx.length; i++) {
            resp = Integer.min(resp, lastIdx[i]);
        }
        return resp;
    }
}
```
