// 899. Binary Gap
// https://leetcode.com/problems/binary-gap/


class Solution {
    public int binaryGap(int n) {
        int resp =0;
        int lastOnepos = 0;
        int currentPos = 1;
        while (n > 0){
            if((n&1) == 1){
                if(lastOnepos > 0 ){
                    //101
                    resp = Integer.max(resp , currentPos - lastOnepos);
                }
                lastOnepos = currentPos;
            }
            n >>=1;
            currentPos++;
        }

        return resp;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[] nData = {22, 8, 5};
        int[] expectedData = {2, 0, 2};

        for (int i = 0; i < nData.length; i++) {
            total++;
            int result = solution.binaryGap(nData[i]);
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
