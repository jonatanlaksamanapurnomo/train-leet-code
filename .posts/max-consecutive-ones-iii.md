# Java | Sliding Window | O(n) flip at most k zeros

## Intuition
Use a sliding window that allows at most `k` zeros. When zero count exceeds `k`, shrink from the left.

## Approach
1. Expand right, counting zeros encountered.
2. While zero count exceeds `k`, shrink from `left`, decrementing zero count if `nums[left]` is 0.
3. Track the maximum window size.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public int longestOnes(int[] nums, int k) {
        int left = 0;
        int longestOnesResp = 0;
        int currentZeroCount = 0;
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == 0) currentZeroCount++;
            while (currentZeroCount > k) {
                if (nums[left] == 0) currentZeroCount--;
                left++;
            }
            longestOnesResp = Integer.max(longestOnesResp, right - left + 1);
        }
        return longestOnesResp;
    }
}
```
