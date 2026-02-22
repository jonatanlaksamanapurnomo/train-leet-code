# Java | Sliding Window + HashMap | O(n) at most 2 fruit types

## Intuition
This is a longest subarray with at most 2 distinct elements problem. Use a sliding window with a HashMap tracking fruit type counts.

## Approach
1. Expand right, adding the fruit type to the map.
2. While map size exceeds 2, shrink from left and remove types with zero count.
3. Track the maximum window size.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(1) — map holds at most 3 entries

## Code
```java
class Solution {
    public int totalFruit(int[] fruits) {
        HashMap<Integer, Integer> cache = new HashMap<>();
        int left = 0;
        int maxFruit = 0;
        for (int right = 0; right < fruits.length; right++) {
            cache.put(fruits[right], cache.getOrDefault(fruits[right], 0) + 1);
            while (cache.size() > 2) {
                cache.put(fruits[left], cache.get(fruits[left]) - 1);
                if (cache.get(fruits[left]) <= 0) cache.remove(fruits[left]);
                left++;
            }
            maxFruit = Integer.max(maxFruit, right - left + 1);
        }
        return maxFruit;
    }
}
```
