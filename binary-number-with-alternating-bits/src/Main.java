// 693. Binary Number with Alternating Bits
// https://leetcode.com/problems/binary-number-with-alternating-bits/

class Solution {
    public boolean hasAlternatingBits(int n) {
        int alternate =  (n >> 1);
        while(alternate > 0){
            int lastAlternateBit = alternate & 1;
            int lastNBit = n & 1;
            int bit = lastAlternateBit ^ lastNBit;
            if(bit != 1){
                return false;
            }
            alternate >>=1;
            n>>=1;
        }
        return true;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[] nData = {5, 7, 11,4};
        boolean[] expectedData = {true, false, false,false};

        for (int i = 0; i < nData.length; i++) {
            total++;
            boolean result = solution.hasAlternatingBits(nData[i]);
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
