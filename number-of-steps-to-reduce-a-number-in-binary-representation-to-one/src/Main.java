// 1520. Number of Steps to Reduce a Number in Binary Representation to One
// https://leetcode.com/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one/

import java.util.BitSet;

class Solution {
    public int numSteps(String s) {
        int count = 0;
        while (s.length() > 1) {
            //Odd , half 2
            if(s.charAt(s.length()-1) == '1') {
                s = addOne(s);
            } else {
                s = divideTwo(s);
            }
            count++;
        }
        return count;
    }

    public static String addOne(String s){
        char[] arr = s.toCharArray();
        for(int i = s.length()-1; i >= 0; i--){
            if(s.charAt(i) == '0'){
                arr[i] = '1';
                return new String(arr);
            }
            else{
                arr[i] = '0';
            }
        }

        return "1" + new String(arr);
    }

    public static String divideTwo(String bits) {
        return bits.substring(0, bits.length() - 1);
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        String[] sData = {"1101", "10", "1"};
        int[] expectedData = {6, 1, 0};

        for (int i = 0; i < sData.length; i++) {
            total++;
            int result = solution.numSteps(sData[i]);
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
