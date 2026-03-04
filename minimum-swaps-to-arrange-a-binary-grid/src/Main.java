// 1658. Minimum Swaps to Arrange a Binary Grid
// https://leetcode.com/problems/minimum-swaps-to-arrange-a-binary-grid/

import java.util.Arrays;

class Solution {
    public int minSwaps(int[][] grid) {
        
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[][][] gridData = {
            new int[][]{{0, 0, 1}, {1, 1, 0}, {1, 0, 0}},
            new int[][]{{0, 1, 1, 0}, {0, 1, 1, 0}, {0, 1, 1, 0}, {0, 1, 1, 0}},
            new int[][]{{1, 0, 0}, {1, 1, 0}, {1, 1, 1}}
        };
        int[] expectedData = {3, -1, 0};

        for (int i = 0; i < gridData.length; i++) {
            total++;
            int result = solution.minSwaps(gridData[i]);
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
