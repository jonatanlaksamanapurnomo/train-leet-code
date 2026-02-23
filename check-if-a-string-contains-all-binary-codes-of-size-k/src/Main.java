// 1557. Check If a String Contains All Binary Codes of Size K
// https://leetcode.com/problems/check-if-a-string-contains-all-binary-codes-of-size-k/

import java.util.HashSet;

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

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        String[] sData = {"00110110", "0110", "0110"};
        int[] kData = {2, 1, 2};
        boolean[] expectedData = {true, true, false};

        for (int i = 0; i < sData.length; i++) {
            total++;
            boolean result = solution.hasAllCodes(sData[i], kData[i]);
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
