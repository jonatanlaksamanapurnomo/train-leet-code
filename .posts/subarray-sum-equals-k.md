# Java | Prefix Sum + Hash Map | O(n) one-pass counting

## Intuition
If the prefix sum up to index `j` minus the prefix sum up to index `i` equals `k`, then the subarray `(i, j]` sums to `k`. We can count how many previous prefix sums equal `sum - k` using a hash map to find all valid subarrays in one pass.

## Approach
1. Initialize a running `sum`, a result counter `ans`, and a hash map storing prefix sum frequencies with `{0: 1}` as the base case.
2. For each element, add it to `sum`.
3. Look up `sum - k` in the map — its frequency is the number of subarrays ending here that sum to `k`. Add that to `ans`.
4. Record the current `sum` in the map by incrementing its frequency.
5. Return `ans`.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(n)

## Code
```java
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
```
