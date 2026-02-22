# Java | Fixed Sliding Window | O(n) running sum

## Intuition
Compute the sum of the first `k` elements, then slide the window by adding the next element and removing the leftmost, tracking the max sum.

## Approach
1. Compute the initial window sum for the first `k` elements.
2. Slide the window: add `nums[right]`, subtract `nums[left]`.
3. Track the maximum sum, return `maxSum / k`.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public double findMaxAverage(int[] nums, int k) {
        double currentWindowSum = 0;
        int left = 0;
        for (int i = 0; i < k; i++) {
            currentWindowSum += nums[i];
        }
        double maxSum = currentWindowSum;
        for (int right = k; right < nums.length; right++) {
            currentWindowSum += nums[right] - nums[left];
            left++;
            maxSum = Double.max(maxSum, currentWindowSum);
        }
        return maxSum / k;
    }
}
```
