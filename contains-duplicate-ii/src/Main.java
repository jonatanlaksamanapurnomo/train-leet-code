// 219. Contains Duplicate II
// https://leetcode.com/problems/contains-duplicate-ii/

import java.util.Arrays;
import java.util.HashMap;

class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        int left = 0;
        HashMap<Integer,Integer> cache = new HashMap<>();


        for(int i = 0 ; i<Math.min(k,nums.length) ; i++){
            if(cache.getOrDefault(nums[i] , 0 ) > 0){
                return true;
            }
            cache.put(nums[i] , cache.getOrDefault(nums[i] , 0) + 1);
        }

        for(int right = k ; right < nums.length ; right++){

            //Shrink window if already > k
            if(right - left + 1 > k+1){
                cache.put(nums[left] , cache.get(nums[left]) - 1);
                left++;
            }

            //Check elm already exist or not
            int currentElm = nums[right];
            if (cache.getOrDefault(currentElm, 0) > 0) {
                return true;
            }

            cache.put(nums[right] ,cache.getOrDefault(nums[right],0) + 1);
        }

        return false;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[][] numsData = {
            new int[]{1, 2, 3, 1},
            new int[]{1, 0, 1, 1},
            new int[]{1, 2, 3, 1, 2, 3}
        };
        int[] kData = {3, 1, 2};
        boolean[] expectedData = {true, true, false};

        for (int i = 0; i < numsData.length; i++) {
            total++;
            boolean result = solution.containsNearbyDuplicate(numsData[i], kData[i]);
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
