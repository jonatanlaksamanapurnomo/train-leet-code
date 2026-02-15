// 209. Minimum Size Subarray Sum
// https://leetcode.com/problems/minimum-size-subarray-sum/

class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left = 0;
        int currentSum = 0;
        int minWindowSize = Integer.MAX_VALUE;
        for(int right = 0 ; right < nums.length ; right++){
            currentSum += nums[right];

            //shrink windows
            while (currentSum >= target){
                int currentWindowSize = (right - left)+1;
                minWindowSize = Integer.min(minWindowSize , currentWindowSize);
                currentSum -= nums[left++];
            }
        }

        if(minWindowSize == Integer.MAX_VALUE){
            return 0;
        }
        return minWindowSize;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();

        // Example 1: target = 7, nums = [2,3,1,2,4,3] -> Output: 2
        System.out.println(solution.minSubArrayLen(7, new int[]{2, 3, 1, 2, 4, 3}));

        // Example 2: target = 4, nums = [1,4,4] -> Output: 1
        System.out.println(solution.minSubArrayLen(4, new int[]{1, 4, 4}));

        // Example 3: target = 11, nums = [1,1,1,1,1,1,1,1] -> Output: 0
        System.out.println(solution.minSubArrayLen(11, new int[]{1, 1, 1, 1, 1, 1, 1, 1}));
    }
}
