// 1458. Sort Integers by The Number of 1 Bits
// https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits/

import java.util.Arrays;
import java.util.PriorityQueue;

class Solution {
    public int[] sortByBits(int[] arr) {
        int [] resp = new int[arr.length];
        PriorityQueue<Integer> pq = new PriorityQueue<Integer>((a,b) -> {
            int bitsA = countOneInBit(a);
            int bitsB = countOneInBit(b);

            if(bitsA == bitsB){
                return a-b;
            }
            return bitsA - bitsB;
        });

        for(int i = 0 ; i<arr.length ; i++){
            pq.add(arr[i]);
        }

        int i = 0;
        while (pq.size() > 0){
            resp[i++] = pq.poll();
        }
        return resp;
    }

    public static int countOneInBit(int elm) {
        int totalOne = 0;

        while (elm > 0 ){
            if((elm & 1) == 1){
                totalOne++;
            }
            elm >>=1;
        }
        return totalOne;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[][] arrData = {
            new int[]{0, 1, 2, 3, 4, 5, 6, 7, 8},
            new int[]{1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1}
        };
        int[][] expectedData = {
            new int[]{0, 1, 2, 4, 8, 3, 5, 6, 7},
            new int[]{1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024}
        };

        for (int i = 0; i < arrData.length; i++) {
            total++;
            int[] result = solution.sortByBits(arrData[i]);
            if (Arrays.equals(result, expectedData[i])) {
                System.out.println("Test " + (i + 1) + ": PASS");
                passed++;
            } else {
                System.out.println("Test " + (i + 1) + ": FAIL (expected: " + Arrays.toString(expectedData[i]) + ", got: " + Arrays.toString(result) + ")");
            }
        }

        System.out.println("\n" + passed + "/" + total + " tests passed.");
    }
}
