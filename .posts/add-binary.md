# Java | Two Pointers | O(max(n,m)) right-to-left addition with carry

## Intuition
Process both strings from right to left, just like manual binary addition — sum digits plus carry, append result bit, propagate carry.

## Approach
1. Start from the last index of both strings.
2. Sum the digits and carry, append `total % 2`, carry = `total / 2`.
3. Move both pointers left. Continue until both are exhausted and carry is 0.
4. Reverse the StringBuilder for the final result.

## Complexity
- **Time complexity:** O(max(n, m))
- **Space complexity:** O(max(n, m))

## Code
```java
class Solution {
    public String addBinary(String a, String b) {
        int lastIdxA = a.length() - 1;
        int lastIdxB = b.length() - 1;
        int carry = 0;
        StringBuilder sb = new StringBuilder();
        while (lastIdxA >= 0 || lastIdxB >= 0 || carry > 0) {
            int aElm = lastIdxA >= 0 ? a.charAt(lastIdxA) - '0' : 0;
            int bElm = lastIdxB >= 0 ? b.charAt(lastIdxB) - '0' : 0;
            int total = carry + aElm + bElm;
            sb.append(total % 2);
            carry = total / 2;
            lastIdxA--;
            lastIdxB--;
        }
        return sb.reverse().toString();
    }
}
```
