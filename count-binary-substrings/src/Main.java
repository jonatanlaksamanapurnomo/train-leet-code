// 696. Count Binary Substrings
// https://leetcode.com/problems/count-binary-substrings/

import java.util.ArrayList;

class Solution {
    public int countBinarySubstrings(String s) {
        ArrayList<Integer> group = new ArrayList<>();
        int currentGroupLen = 1;
        int resp = 0;

        for(int i = 1; i<s.length();i++){
            char prev = s.charAt(i-1);
            char current = s.charAt(i);

            if(prev == current){
                currentGroupLen++;
            }
            else {
                group.add(currentGroupLen);
                currentGroupLen = 1;
            }
        }
        group.add(currentGroupLen);

        for(int i = 1; i<group.size() ; i++){
            int current = group.get(i);
            int prev = group.get(i-1);
            resp += Integer.min(current , prev);
        }
        return resp;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        String[] sData = {"00110011", "10101"};
        int[] expectedData = {6, 4};

        for (int i = 0; i < sData.length; i++) {
            total++;
            int result = solution.countBinarySubstrings(sData[i]);
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
