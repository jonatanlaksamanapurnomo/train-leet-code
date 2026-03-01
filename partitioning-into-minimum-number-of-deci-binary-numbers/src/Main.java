// 1807. Partitioning Into Minimum Number Of Deci-Binary Numbers
// https://leetcode.com/problems/partitioning-into-minimum-number-of-deci-binary-numbers/

class Solution {
    public int minPartitions(String n) {
        int maxNumber = 0;

        for(int i = 0 ; i<n.length() ; i++){
            int currentValue = Integer.parseInt(n.charAt(i) + "");
            maxNumber = Integer.max(maxNumber , currentValue);
        }

        return maxNumber;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        String[] nData = {"32", "82734", "27346209830709182346"};
        int[] expectedData = {3, 8, 9};

        for (int i = 0; i < nData.length; i++) {
            total++;
            int result = solution.minPartitions(nData[i]);
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
