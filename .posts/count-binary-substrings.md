# Java | Grouping | O(n) count consecutive groups

## Intuition
Group consecutive identical characters. The number of valid substrings between two adjacent groups is the minimum of their lengths.

## Approach
1. Traverse the string and group consecutive characters by their run length.
2. For each pair of adjacent groups, add `min(group[i], group[i-1])` to the result.

## Complexity
- **Time complexity:** O(n)
- **Space complexity:** O(n) for the group list (can be optimized to O(1))

## Code
```java
class Solution {
    public int countBinarySubstrings(String s) {
        ArrayList<Integer> group = new ArrayList<>();
        int currentGroupLen = 1;
        int resp = 0;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i - 1) == s.charAt(i)) {
                currentGroupLen++;
            } else {
                group.add(currentGroupLen);
                currentGroupLen = 1;
            }
        }
        group.add(currentGroupLen);
        for (int i = 1; i < group.size(); i++) {
            resp += Integer.min(group.get(i), group.get(i - 1));
        }
        return resp;
    }
}
```
