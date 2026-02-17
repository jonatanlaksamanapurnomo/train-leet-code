// 401. Binary Watch
// https://leetcode.com/problems/binary-watch/

import java.util.ArrayList;
import java.util.List;

class Solution {
    public List<String> readBinaryWatch(int turnedOn) {
        List<String> result = new ArrayList<>();

        for(int h = 0 ; h<=11; h++){
            for(int m = 0 ; m<=59 ; m++){
                if(Integer.bitCount(h) + Integer.bitCount(m) == turnedOn){
                    result.add(h + ":" + (m < 10 ? "0" + m : m));
                }
            }
        }

        return result;
    }

}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[] turnedOnData = {1, 9};
        @SuppressWarnings("unchecked")
        List<String>[] expectedData = new List[]{
            List.of("0:01", "0:02", "0:04", "0:08", "0:16", "0:32", "1:00", "2:00", "4:00", "8:00"),
            List.of()
        };

        for (int i = 0; i < turnedOnData.length; i++) {
            total++;
            List<String> result = solution.readBinaryWatch(turnedOnData[i]);
            if (result.equals(expectedData[i])) {
                System.out.println("Test " + (i + 1) + ": PASS");
                passed++;
            } else {
                System.out.println("Test " + (i + 1) + ": FAIL (expected: " + expectedData[i] + ", got: " + result + ")");
            }
        }

        System.out.println("\n" + passed + "/" + total + " tests passed.");
    }
}
