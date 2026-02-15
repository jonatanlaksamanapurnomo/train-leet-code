// 643. Maximum Average Subarray I
// https://leetcode.com/problems/maximum-average-subarray-i/

class Solution {
    public double findMaxAverage(int[] nums, int k) {
        double currentWindowSum = 0;
        int left = 0;

        for(int i = 0 ; i < k ;i++){
            currentWindowSum += nums[i];
        }

        double maxSum = currentWindowSum;
        for(int right = k ; right < nums.length ; right++){
            currentWindowSum += nums[right] - nums[left];
            left++;
            maxSum = Double.max(maxSum,currentWindowSum);
        }

        return maxSum/k;
    }

}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        // Test 1: nums = [1,12,-5,-6,50,3], k = 4 -> Expected: 12.75000
        total++;
        double result1 = solution.findMaxAverage(new int[]{1, 12, -5, -6, 50, 3}, 4);
        double expected1 = 12.75000;
        if (Math.abs(result1 - expected1) < 1e-5) {
            System.out.println("Test 1: PASS");
            passed++;
        } else {
            System.out.println("Test 1: FAIL (expected: " + expected1 + ", got: " + result1 + ")");
        }

        // Test 2: nums = [5], k = 1 -> Expected: 5.00000
        total++;
        double result2 = solution.findMaxAverage(new int[]{5}, 1);
        double expected2 = 5.00000;
        if (Math.abs(result2 - expected2) < 1e-5) {
            System.out.println("Test 2: PASS");
            passed++;
        } else {
            System.out.println("Test 2: FAIL (expected: " + expected2 + ", got: " + result2 + ")");
        }

        total++;
        double result3 = solution.findMaxAverage(new int[]{-1}, 1);
        double expected3 = -1;
        if (Math.abs(result3 - expected3) < 1e-5) {
            System.out.println("Test 3: PASS");
            passed++;
        } else {
            System.out.println("Test 3: FAIL (expected: " + expected3 + ", got: " + result3 + ")");
        }


        System.out.println("\n" + passed + "/" + total + " tests passed.");
    }
}
