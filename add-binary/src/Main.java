// 67. Add Binary
// https://leetcode.com/problems/add-binary/

class Solution {
    public String addBinary(String a, String b) {
        int lastIdxA = a.length() - 1;
        int lastIdxB = b.length()-1;
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

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();


        // Example 1: a = "11", b = "1" -> Output: "100"
        System.out.println(solution.addBinary("11", "1"));

        // Example 2: a = "1010", b = "1011" -> Output: "10101"
        System.out.println(solution.addBinary("1010", "1011"));
    }
}
