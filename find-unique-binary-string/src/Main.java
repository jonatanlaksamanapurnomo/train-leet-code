// 2107. Find Unique Binary String
// https://leetcode.com/problems/find-unique-binary-string/

import java.util.Arrays;

class Solution {
    public String findDifferentBinaryString(String[] nums) {
        StringBuilder diagonal = new StringBuilder();
        for(int i = 0; i < nums.length; i++){
            String currentNum = nums[i];
            for(int j = 0 ; j<currentNum.length() ; j++){
                if(j == i){
                    diagonal.append(flipChar(currentNum.charAt(j)));
                    break;
                }
            }
        }
        return diagonal.toString();
    }

    public char flipChar(char ch){
        if(ch == '1') return '0';
        return '1';
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        String[][] numsData = {
            new String[]{"01", "10"},
            new String[]{"00", "01"},
            new String[]{"111", "011", "001"}
        };
        String[] expectedData = {"11", "11", "101"};

        for (int i = 0; i < numsData.length; i++) {
            total++;
            String result = solution.findDifferentBinaryString(numsData[i]);
            if (result.equals(expectedData[i])) {
                System.out.println("Test " + (i + 1) + ": PASS");
                passed++;
            } else {
                System.out.println("Test " + (i + 1) + ": FAIL (expected: " + expectedData[i] + ", got: " + result + ")");
            }
        }

        System.out.println("\n" + passed + "/" + total + " tests passed.");
    }
}
