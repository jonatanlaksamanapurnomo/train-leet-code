// 940. Fruit Into Baskets
// https://leetcode.com/problems/fruit-into-baskets/

import java.util.Arrays;
import java.util.HashMap;

class Solution {
    public int totalFruit(int[] fruits) {
        HashMap<Integer,Integer> cache = new HashMap<>();
        int left = 0;
        int maxFruit = 0;

        for(int right = 0 ; right < fruits.length ; right++){

            //Add to cache
            cache.put(fruits[right] , cache.getOrDefault(fruits[right] , 0) +1);

            //Shrink window
            while (cache.size() > 2 ){
                cache.put(fruits[left] , cache.get(fruits[left])-1);
                if(cache.get(fruits[left]) <= 0 ){
                    cache.remove(fruits[left]);
                }
                left++;
            }

            //Calc response
            maxFruit = Integer.max(maxFruit , right - left +1);

        }


        return maxFruit;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[][] fruitsData = {
            new int[]{1, 2, 1},
            new int[]{0, 1, 2, 2},
            new int[]{1, 2, 3, 2, 2}, new int[]{3,3,3,1,2,1,1,2,3,3,4}
        };
        int[] expectedData = {3, 3, 4,5};

        for (int i = 0; i < fruitsData.length; i++) {
            total++;
            int result = solution.totalFruit(fruitsData[i]);
            if (result == expectedData[i]) {
                System.out.println("Test " + (i + 1) + ": PASS");
                passed++;
            } else {
                System.out.println("Test " + (i + 1) + ": FAIL (expected: " + expectedData[i] + ", got: " + result + ")");
            }
        }

        System.out.println("\n" + passed + "/" + total + " tests passed.");
    }
}
