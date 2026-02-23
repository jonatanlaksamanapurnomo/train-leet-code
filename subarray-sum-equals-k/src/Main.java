// 560. Subarray Sum Equals K
// https://leetcode.com/problems/subarray-sum-equals-k/

import java.util.HashMap;

class Solution {
    public int subarraySum(int[] nums, int k) {
        int sum = 0;
        HashMap<Integer, Integer> cache = new HashMap<>();
        int ans = 0;

        cache.put(0, 1);

        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];

            ans += cache.getOrDefault(sum - k, 0);

            cache.put(sum, cache.getOrDefault(sum, 0) + 1);
        }

        return ans;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[][] numsData = {
                new int[]{1, 1, 1},
                new int[]{1, 2, 3},
                new int[]{1, -1, 1, 1, 1}
        };
        int[] kData = {2, 3, 2};
        int[] expectedData = {2, 2, 4};

        for (int i = 0; i < numsData.length; i++) {
            total++;
            int result = solution.subarraySum(numsData[i], kData[i]);
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
