// 1046. Max Consecutive Ones III
// https://leetcode.com/problems/max-consecutive-ones-iii/

import java.util.Arrays;

class Solution {
    public int longestOnes(int[] nums, int k) {
        int left = 0;
        int longestOnesResp = 0;

        int currentZeroCount = 0;

        for(int right = 0 ; right < nums.length ; right++){
            //Flag logic
            if(nums[right] == 0 ){
                currentZeroCount++;
            }
            //Shrink logic, if total zero > k means we need to shrink window
            while (currentZeroCount > k){
                if(nums[left] == 0 ){
                    currentZeroCount--;
                }
                left++;
            }
            //update result first, base on current window size
            longestOnesResp = Integer.max(longestOnesResp , right - left + 1);
        }

        return longestOnesResp;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();

        // Example 1: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2 -> Output: 6
        System.out.println(solution.longestOnes(new int[]{1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0}, 2));

        // Example 2: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3 -> Output: 10
        System.out.println(solution.longestOnes(new int[]{0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1}, 3));
    }
}
