// 190. Reverse Bits
// https://leetcode.com/problems/reverse-bits/

class Solution {
    public int reverseBits(int n) {
        int result = 0;

        for(int i = 0 ; i < 32 ; i++){
            result = (result << 1) |(n&1);
            n>>=1;
        }
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[] nData = {43261596, 2147483644};
        int[] expectedData = {964176192, 1073741822};

        for (int i = 0; i < nData.length; i++) {
            total++;
            int result = solution.reverseBits(nData[i]);
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
