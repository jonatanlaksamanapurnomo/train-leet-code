# Java | Sliding Window + HashMap | O(n) window of size k

## Intuition
Maintain a sliding window of size `k` with a frequency map. If any element already exists in the window when we try to add it, we found a duplicate within distance `k`.

## Approach
1. Use a HashMap to track element frequencies within the current window.
2. Expand right, check if element already exists in window.
3. Shrink from left when window exceeds size `k+1`.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(k)

## Code
```java
class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        int left = 0;
        HashMap<Integer, Integer> cache = new HashMap<>();
        for (int i = 0; i < Math.min(k, nums.length); i++) {
            if (cache.getOrDefault(nums[i], 0) > 0) return true;
            cache.put(nums[i], cache.getOrDefault(nums[i], 0) + 1);
        }
        for (int right = k; right < nums.length; right++) {
            if (right - left + 1 > k + 1) {
                cache.put(nums[left], cache.get(nums[left]) - 1);
                left++;
            }
            if (cache.getOrDefault(nums[right], 0) > 0) return true;
            cache.put(nums[right], cache.getOrDefault(nums[right], 0) + 1);
        }
        return false;
    }
}
```
