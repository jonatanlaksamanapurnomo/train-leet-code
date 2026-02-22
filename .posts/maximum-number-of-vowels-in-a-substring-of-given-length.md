# Java | Fixed Sliding Window | O(n) vowel count tracking

## Intuition
Use a fixed-size sliding window of length `k`, tracking the vowel count. Slide by adding/removing one character at a time.

## Approach
1. Count vowels in the first `k` characters.
2. Slide the window: add 1 if new char is vowel, subtract 1 if removed char is vowel.
3. Track the maximum vowel count.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public int maxVowels(String s, int k) {
        int maxVowel = 0;
        int left = 0;
        for (int i = 0; i < k; i++) {
            if (isCharVowel(s.charAt(i))) maxVowel++;
        }
        int currentVowel = maxVowel;
        for (int right = k; right < s.length(); right++) {
            int add = isCharVowel(s.charAt(right)) ? 1 : 0;
            int remove = isCharVowel(s.charAt(left)) ? 1 : 0;
            currentVowel += add - remove;
            maxVowel = Integer.max(maxVowel, currentVowel);
            left++;
        }
        return maxVowel;
    }

    public boolean isCharVowel(char c) {
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    }
}
```
