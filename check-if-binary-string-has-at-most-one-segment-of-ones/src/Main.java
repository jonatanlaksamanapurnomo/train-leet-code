// 1910. Check if Binary String Has at Most One Segment of Ones
// https://leetcode.com/problems/check-if-binary-string-has-at-most-one-segment-of-ones/

class Solution {
    public boolean checkOnesSegment(String s) {
        boolean seenZero = false;
        for(int i = 0; i < s.length(); i++) {
            if(s.charAt(i) == '0') {
                seenZero = true;
            } else {
                if(seenZero) {
                    return false;
                }
            }
        }
        return true;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        String[] sData = {"1001", "110","1"};
        boolean[] expectedData = {false, true,true};

        for (int i = 0; i < sData.length; i++) {
            total++;
            boolean result = solution.checkOnesSegment(sData[i]);
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
