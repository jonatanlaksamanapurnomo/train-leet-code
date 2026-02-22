# Java | Sliding Window + HashMap | O(n) character frequency tracking

## Intuition
Maintain a sliding window with a frequency map. When a duplicate is found, shrink from the left until all characters are unique again.

## Approach
1. Use a HashMap to track character frequencies in the current window.
2. For each `right`, increment the frequency. If it exceeds 1, shrink from `left` until it's back to 1.
3. Update the max length at each step.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(min(n, 26)) for the character map

## Code
```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> cache = new HashMap<>();
        int left = 0;
        int longestSubstring = 0;
        for (int right = 0; right < s.length(); right++) {
            cache.put(s.charAt(right), cache.getOrDefault(s.charAt(right), 0) + 1);
            while (cache.get(s.charAt(right)) > 1) {
                cache.put(s.charAt(left), cache.get(s.charAt(left)) - 1);
                left++;
            }
            longestSubstring = Integer.max(longestSubstring, right - left + 1);
        }
        return longestSubstring;
    }
}
```
