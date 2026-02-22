# Java | Sliding Window | O(n) max frequency character tracking

## Intuition
In any valid window, the number of characters to replace is `windowSize - maxFreq`. If this exceeds `k`, shrink the window.

## Approach
1. Track character frequencies and the max frequency in the current window.
2. Expand right, updating frequency and maxFreq.
3. While `windowSize - maxFreq > k`, shrink from left.
4. Track the maximum window size.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(1) — frequency array of size 26

## Code
```java
class Solution {
    public int characterReplacement(String s, int k) {
        int longestCharLen = 0;
        int left = 0;
        int[] freq = new int[26];
        int maxFreq = 0;
        for (int right = 0; right < s.length(); right++) {
            freq[s.charAt(right) - 'A']++;
            maxFreq = Integer.max(maxFreq, freq[s.charAt(right) - 'A']);
            while (right - left + 1 - maxFreq > k) {
                freq[s.charAt(left) - 'A']--;
                left++;
            }
            longestCharLen = Integer.max(longestCharLen, right - left + 1);
        }
        return longestCharLen;
    }
}
```
