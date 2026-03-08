# Java | Row & Column Counting | O(m·n) single-pass precompute

## Intuition
A position is "special" only if it's `1` and the only `1` in both its row and column. We can determine this efficiently by pre-counting the number of `1`s in each row and column.

## Approach
1. Create `rowCount` and `colCount` arrays to store the number of `1`s in each row and column.
2. In a single nested loop, accumulate counts for both arrays simultaneously.
3. In a second pass, check each cell: if `mat[i][j] == 1` and `rowCount[i] == 1` and `colCount[j] == 1`, it's a special position.
4. Return the total count.

## Complexity
- **Time complexity:** O(m·n) — two passes over the matrix.
- **Space complexity:** O(m+n) — for the row and column count arrays.

## Code
```java
class Solution {
    public int numSpecial(int[][] mat) {
        int [] rowCount = new int [mat.length];
        int [] colCount = new int [mat[0].length];

        for(int i = 0; i < mat.length; i++){
            for(int j = 0; j < mat[0].length; j++){
                rowCount[i] += mat[i][j];
                colCount[j] += mat[i][j];
            }
        }

        int count = 0;
        for(int i = 0; i < mat.length; i++){
            for(int j = 0; j < mat[0].length; j++){
                if(mat[i][j] == 1 && rowCount[i] == 1 && colCount[j] == 1){
                    count++;
                }
            }
        }

        return count;
    }
}
```
