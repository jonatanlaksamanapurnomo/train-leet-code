// 1704. Special Positions in a Binary Matrix
// https://leetcode.com/problems/special-positions-in-a-binary-matrix/

import java.util.Arrays;

class Solution {
    public int numSpecial(int[][] mat) {
        int [] rowCount = new int [mat.length];
        int [] colCount = new int [mat[0].length];

        // Hitung semua 1 per row dan per col dalam 1 loop
        for(int i = 0; i < mat.length; i++){
            for(int j = 0; j < mat[0].length; j++){
                rowCount[i] += mat[i][j];  // akumulasi per row
                colCount[j] += mat[i][j];  // akumulasi per col
            }
        }

        int count = 0;
        for(int i = 0; i < mat.length; i++){
            for(int j = 0; j < mat[0].length; j++){
                if(mat[i][j] == 1 && rowCount[i] == 1 && colCount[j] == 1){
                    count++;
                }
            }
        }

        return count;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[][][] matData = {
            new int[][]{{1, 0, 0}, {0, 0, 1}, {1, 0, 0}},
            new int[][]{{1, 0, 0}, {0, 1, 0}, {0, 0, 1}}
        };
        int[] expectedData = {1, 3};

        for (int i = 0; i < matData.length; i++) {
            total++;
            int result = solution.numSpecial(matData[i]);
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
