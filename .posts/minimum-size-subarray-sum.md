# Java | Sliding Window | O(n) shrink when sum meets target

## Intuition
Use a sliding window that expands right and shrinks from the left whenever the window sum meets or exceeds the target, tracking the minimum window size.

## Approach
1. Expand the window by adding `nums[right]` to `currentSum`.
2. While `currentSum >= target`, record the window size and shrink by removing `nums[left]`.
3. Return the minimum window size found, or 0 if none.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left = 0;
        int currentSum = 0;
        int minWindowSize = Integer.MAX_VALUE;
        for (int right = 0; right < nums.length; right++) {
            currentSum += nums[right];
            while (currentSum >= target) {
                int currentWindowSize = (right - left) + 1;
                minWindowSize = Integer.min(minWindowSize, currentWindowSize);
                currentSum -= nums[left++];
            }
        }
        if (minWindowSize == Integer.MAX_VALUE) return 0;
        return minWindowSize;
    }
}
```
