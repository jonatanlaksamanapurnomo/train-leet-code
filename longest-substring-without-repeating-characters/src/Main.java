// 3. Longest Substring Without Repeating Characters
// https://leetcode.com/problems/longest-substring-without-repeating-characters/

import java.util.HashMap;
import java.util.Map;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character,Integer> cache = new HashMap<>();
        int left = 0;
        int longestSubstring = Integer.MIN_VALUE;


        for(int right = 0 ; right < s.length() ; right++){
            //if key not exist or 0 add
            cache.put(s.charAt(right) , cache.getOrDefault(s.charAt(right) , 0) + 1);

            while (cache.get(s.charAt(right)) > 1){
                cache.put(s.charAt(left), cache.get(s.charAt(left)) - 1);
                left++;
            }

            longestSubstring = Integer.max(longestSubstring , right - left + 1);

        }

        System.out.println(cache);
        return longestSubstring;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();

        // Example 1: s = "abcabcbb" -> Output: 3
        System.out.println(solution.lengthOfLongestSubstring("abcabcbb"));

        // Example 2: s = "bbbbb" -> Output: 1
        System.out.println(solution.lengthOfLongestSubstring("bbbbb"));

        // Example 3: s = "pwwkew" -> Output: 3
        System.out.println(solution.lengthOfLongestSubstring("pwwkew"));
    }
}
