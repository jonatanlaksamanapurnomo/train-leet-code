# Java | Greedy | O(n) max digit

## Intuition
Each deci-binary number can contribute at most 1 to any digit position. Therefore, the minimum number of deci-binary numbers needed equals the largest digit in the string.

## Approach
1. Iterate through each character in the string `n`.
2. Convert each character to its numeric value.
3. Track the maximum digit encountered.
4. Return the maximum digit as the answer.

## Complexity
- **Time complexity:** O(n), where n is the length of the string.
- **Space complexity:** O(1)

## Code
```java
class Solution {
    public int minPartitions(String n) {
        int maxNumber = 0;

        for(int i = 0 ; i<n.length() ; i++){
            int currentValue = Integer.parseInt(n.charAt(i) + "");
            maxNumber = Integer.max(maxNumber , currentValue);
        }

        return maxNumber;
    }
}
```
