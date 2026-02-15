// 1567. Maximum Number of Vowels in a Substring of Given Length
// https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/

class Solution {
    public int maxVowels(String s, int k) {
        int maxVowel = 0;
        int left = 0;

        for(int i = 0; i < k ; i++){
            char currentChar = s.charAt(i);
            if(isCharVowel(currentChar)){
                maxVowel++;
            }
        }

        int currentVowel = maxVowel;
        for(int right = k ; right < s.length() ; right++){
            int add = isCharVowel(s.charAt(right)) ? 1 : 0;
            int remove = isCharVowel(s.charAt(left)) ? 1:0;
            currentVowel += add - remove;
            maxVowel = Integer.max(maxVowel,currentVowel);
            left++;
        }

        return maxVowel;
    }

    public boolean isCharVowel(char currentChar){
        if(currentChar == 'a' || currentChar == 'i' || currentChar == 'e' || currentChar == 'o' || currentChar=='u'){
            return true;
        }

        return false;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int passed = 0;
        int total = 0;

        String[] sData = {"abciiidef", "aeiou", "leetcode"};
        int[] kData = {3, 2, 3};
        int[] expectedData = {3, 2, 2};

        for (int i = 0; i < sData.length; i++) {
            total++;
            int result = solution.maxVowels(sData[i], kData[i]);
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
