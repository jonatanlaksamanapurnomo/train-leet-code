# It seems write permissions haven't been granted yet. Let me provide the solution post directly.

Here's the post:

---

Java | Greedy | O(n²) Trailing Zeros + Bubble Swap

## Intuition
For the grid to have all zeros above the main diagonal, row `i` must have at least `n-1-i` trailing zeros. We reduce the 2D problem to a 1D greedy problem by computing trailing zeros per row, then greedily bubble the nearest qualifying row into each position.

## Approach
1. Compute the number of trailing zeros for each row.
2. For each row position `i` (top to bottom), determine the required trailing zeros: `n - 1 - i`.
3. Find the first row at index `j >= i` that meets the requirement.
4. If no such row exists, return `-1`.
5. Bubble that row up from `j` to `i` using adjacent swaps, adding `j - i` to the swap count.

## Complexity
- **Time complexity:** O(n²) — for each of the n rows, we may scan and bubble up to n positions.
- **Space complexity:** O(n) — for the trailing zeros array.

## Code
```java
class Solution {
    public int minSwaps(int[][] grid) {
        int n = grid.length;
        int[] trailingZeros = new int[n];
        for (int i = 0; i < n; i++) {
            int count = 0;
            for (int j = n - 1; j >= 0 && grid[i][j] == 0; j--) {
                count++;
            }
            trailingZeros[i] = count;
        }

        int swaps = 0;
        for (int i = 0; i < n; i++) {
            int need = n - 1 - i;
            int j = i;
            while (j < n && trailingZeros[j] < need) {
                j++;
            }
            if (j == n) return -1;
            while (j > i) {
                int tmp = trailingZeros[j];
                trailingZeros[j] = trailingZeros[j - 1];
                trailingZeros[j - 1] = tmp;
                j--;
                swaps++;
            }
        }
        return swaps;
    }
}
```
