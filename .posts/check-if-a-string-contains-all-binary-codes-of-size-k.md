# Java | Sliding Window + HashSet | O(n·k) substring collection

## Intuition
Every binary code of size `k` must appear as a contiguous substring. There are exactly `2^k` such codes, so we slide a window of size `k` across the string, collect all distinct substrings, and check if we've seen all of them.

## Approach
1. Initialize a `HashSet` to store unique substrings and a `left` pointer at 0.
2. Slide `right` from `k-1` to the end of the string, extracting each substring of length `k`.
3. Add each substring to the set.
4. If the set size reaches `2^k`, return `true` early.
5. If the loop ends without reaching `2^k` unique substrings, return `false`.

## Complexity
- **Time complexity:** O(n · k) — we extract n − k + 1 substrings, each of length k.
- **Space complexity:** O(2^k · k) — at most 2^k unique strings of length k stored in the set.

## Code
```java
class Solution {
    public boolean hasAllCodes(String s, int k) {
        int left = 0;
        HashSet<String> set = new HashSet<>();

        for(int right = k-1 ; right < s.length() ; right++){
            String current = s.substring(left , right+1);
            set.add(current);
            if(set.size() == Math.pow(2,k)){
                return true;
            }
            left++;
        }

        return set.size() == Math.pow(2,k) ? true : false;
    }
}
```
