// 767. Prime Number of Set Bits in Binary Representation
// https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/

class Solution {
    static int countPrimeSetBits(int left, int right) {
        int resp = 0;
        for (int i = left; i <= right; i++) {
            int currTotalOne = countOnes(i);
            if (isPrime(currTotalOne)) {
                resp++;
            }
        }

        return resp;
    }

    private static int countOnes(int n) {
        int count = 0;
        while (n > 0) {
            count += n & 1;
            n >>= 1;
        }

        return count;
    }

    private static boolean isPrime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        for (int i = 5; i * i <= n; i += 6) if (n % i == 0 || n % (i + 2) == 0) return false;
        return true;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        int[] leftData = {6, 10};
        int[] rightData = {10, 15};
        int[] expectedData = {4, 5};

        for (int i = 0; i < leftData.length; i++) {
            total++;
            int result = Solution.countPrimeSetBits(leftData[i], rightData[i]);
            if (result == expectedData[i]) {
                System.out.println("Test " + (i + 1) + ": PASS");
                passed++;
            } else
                System.out.println("Test " + (i + 1) + ": FAIL (expected: " + expectedData[i] + ", got: " + result + ")");
        }

        System.out.println("\n" + passed + "/" + total + " tests passed.");
    }
}
