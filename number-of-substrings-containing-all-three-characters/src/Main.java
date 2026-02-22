// 1460. Number of Substrings Containing All Three Characters
// https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/

import java.util.Arrays;

class Solution {
    public int numberOfSubstrings(String s) {
        int []lastIdx = new int[]{-1,-1,-1};
        int resp = 0;

        for(int i = 0; i<s.length(); i++){
            int charToIdx = s.charAt(i) - 'a';
            lastIdx[charToIdx]=i;

            //If Valid a,b,c in set check last idx and +1;
            if(validCharSet(lastIdx)){
                int smallestIdx = getSmallestIdx(lastIdx);
                resp += smallestIdx +1;
            }
        }
        return resp;
    }

    public static boolean  validCharSet(int [] lastIdx){
        for(int i = 0 ; i<lastIdx.length ; i++){
            if(lastIdx[i] == -1){
                return false;
            }
        }
        return true;
    }

    public static int getSmallestIdx(int [] lastIdx){
        int resp = Integer.MAX_VALUE;
        for(int i = 0; i<lastIdx.length ; i++ ){
            resp = Integer.min(resp , lastIdx[i]);
        }
        return resp;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        String[] sData = {"abcabc", "aaacb", "abc"};
        int[] expectedData = {10, 3, 1};

        for (int i = 0; i < sData.length; i++) {
            total++;
            int result = solution.numberOfSubstrings(sData[i]);
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
