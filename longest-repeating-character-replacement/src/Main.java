// 424. Longest Repeating Character Replacement
// https://leetcode.com/problems/longest-repeating-character-replacement/

import java.util.Arrays;

class Solution {
    public int characterReplacement(String s, int k) {
        int longestCharLen = 0;
        int left = 0;
        int [] freq = new int[26];
        int maxFreq = 0;
        for(int right = 0 ; right < s.length() ; right++){
            freq[s.charAt(right) - 'A']++;
            //Shrink
            int freqLeft = freq[s.charAt(right) - 'A'];
            maxFreq = Integer.max(maxFreq , freqLeft);
            while(right - left + 1 - maxFreq  > k){
                freq[s.charAt(left) - 'A']--;
                left++;
            }

            longestCharLen = Integer.max(longestCharLen , right - left + 1);
        }

        return longestCharLen;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        //AAAABBCCCCCCCCCCCCC
        String[] sData = {"ABAB", "AABABBA" , "BAAA","ABBB"};
        int[] kData = {2, 1,0,2};
        int[] expectedData = {4, 4,3,4};

        for (int i = 0; i < sData.length; i++) {
            total++;
            int result = solution.characterReplacement(sData[i], kData[i]);
            if (result == expectedData[i]) {
                System.out.println("Test " + (i + 1) + ": PASS");
                passed++;
            } else {
                System.out.println("Test " + (i + 1) + ": FAIL (expected: " + expectedData[i] + ", got: " + result + ")");
            }
        }

        System.out.println("\n" + passed + "/" + total + " tests passed.");
    }
}
