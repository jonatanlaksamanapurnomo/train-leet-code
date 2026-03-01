# Java | Bit Manipulation + Priority Queue | O(n log n) custom comparator

## Intuition
Use a min-heap with a custom comparator that first compares numbers by their set bit count (popcount), then by value for ties.

## Approach
1. Create a `PriorityQueue` with a comparator that counts 1-bits for each pair of elements — if counts differ, sort by count; otherwise sort by value.
2. Add all elements from the input array into the priority queue.
3. Poll elements one by one into the result array, which yields them in sorted order.
4. Count bits manually by checking the least significant bit (`n & 1`) and right-shifting until zero.

## Complexity
- **Time complexity:** O(n log n) — each insertion/extraction from the heap is O(log n), and bit counting is O(log M) where M is the max value.
- **Space complexity:** O(n) — for the priority queue and result array.

## Code
```java
class Solution {
    public int[] sortByBits(int[] arr) {
        int [] resp = new int[arr.length];
        PriorityQueue<Integer> pq = new PriorityQueue<Integer>((a,b) -> {
            int bitsA = countOneInBit(a);
            int bitsB = countOneInBit(b);

            if(bitsA == bitsB){
                return a-b;
            }
            return bitsA - bitsB;
        });

        for(int i = 0 ; i<arr.length ; i++){
            pq.add(arr[i]);
        }

        int i = 0;
        while (pq.size() > 0){
            resp[i++] = pq.poll();
        }
        return resp;
    }

    public static int countOneInBit(int elm) {
        int totalOne = 0;

        while (elm > 0 ){
            if((elm & 1) == 1){
                totalOne++;
            }
            elm >>=1;
        }
        return totalOne;
    }
}
```
