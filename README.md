# LeetCode Training

My journey solving 81 LeetCode problems, organized by pattern and topic — not by difficulty.

> **Philosophy:** Understand *why* an approach works, not memorize solutions.
> For every problem, ask: "Is it monotonic or not? Why?"

<!-- PROGRESS-START -->
## Progress: 21 / 81 solved

```
Phase 1  Sliding Window        ██████████  9/9
Phase 2  Prefix Sum + HashMap  █░░░░░░░░░  1/7
Phase 3  Two Pointers          ░░░░░░░░░░  0/4
Phase 4  Monotonic Stack       ░░░░░░░░░░  0/4
Phase 5  Binary Search         ░░░░░░░░░░  0/5
Phase 6  Dynamic Programming   ░░░░░░░░░░  0/15
Phase 7  Graph (BFS/DFS)       ░░░░░░░░░░  0/9
Phase 8  Tree                  ░░░░░░░░░░  0/9
Phase 9  Backtracking          ░░░░░░░░░░  0/5
Phase 10 Heap / Priority Queue ░░░░░░░░░░  0/4
Phase 11 Advanced (UF/Trie)    ░░░░░░░░░░  0/10
```
<!-- PROGRESS-END -->

<!-- SOLUTIONS-START -->
## Solutions

| # | Problem | Difficulty | Pattern | Solution |
|---|---------|------------|---------|----------|
| 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Sliding Window | [Java](longest-substring-without-repeating-characters/src/Main.java) |
| 67 | [Add Binary](https://leetcode.com/problems/add-binary/) | Easy | Bit Manipulation | [Java](add-binary/src/Main.java) |
| 190 | [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | Easy | Bit Manipulation | [Java](reverse-bits/src/Main.java) |
| 209 | [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | Sliding Window | [Java](minimum-size-subarray-sum/src/Main.java) |
| 219 | [Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | Easy | Sliding Window | [Java](contains-duplicate-ii/src/Main.java) |
| 401 | [Binary Watch](https://leetcode.com/problems/binary-watch/) | Easy | Backtracking | [Java](binary-watch/src/Main.java) |
| 424 | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium | Sliding Window | [Java](longest-repeating-character-replacement/src/Main.java) |
| 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Prefix Sum | [Java](subarray-sum-equals-k/src/Main.java) |
| 643 | [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | Easy | Sliding Window | [Java](maximum-average-subarray-i/src/Main.java) |
| 693 | [Binary Number with Alternating Bits](https://leetcode.com/problems/binary-number-with-alternating-bits/) | Easy | Bit Manipulation | [Java](binary-number-with-alternating-bits/src/Main.java) |
| 696 | [Count Binary Substrings](https://leetcode.com/problems/count-binary-substrings/) | Easy | Two Pointers | [Java](count-binary-substrings/src/Main.java) |
| 767 | [Prime Number of Set Bits in Binary Representation](https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/) | Easy | Bit Manipulation | [Java](prime-number-of-set-bits-in-binary-representation/src/Main.java) |
| 899 | [Binary Gap](https://leetcode.com/problems/binary-gap/) | Easy | Bit Manipulation | [Java](binary-gap/src/Main.java) |
| 940 | [Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/) | Medium | Sliding Window | [Java](fruit-into-baskets/src/Main.java) |
| 1046 | [Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | Medium | Sliding Window | [Java](max-consecutive-ones-iii/src/Main.java) |
| 1458 | [Sort Integers by The Number of 1 Bits](https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits/) | Easy | Bit Manipulation | [Java](sort-integers-by-the-number-of-1-bits/src/Main.java) |
| 1460 | [Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/) | Medium | Sliding Window | [Java](number-of-substrings-containing-all-three-characters/src/Main.java) |
| 1520 | [Number of Steps to Reduce a Number in Binary Representation to One](https://leetcode.com/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one/) | Medium | Bit Manipulation | [Java](number-of-steps-to-reduce-a-number-in-binary-representation-to-one/src/Main.java) |
| 1557 | [Check If a String Contains All Binary Codes of Size K](https://leetcode.com/problems/check-if-a-string-contains-all-binary-codes-of-size-k/) | Medium | Bit Manipulation | [Java](check-if-a-string-contains-all-binary-codes-of-size-k/src/Main.java) |
| 1567 | [Maximum Number of Vowels in a Substring of Given Length](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) | Medium | Sliding Window | [Java](maximum-number-of-vowels-in-a-substring-of-given-length/src/Main.java) |
| 1807 | [Partitioning Into Minimum Number Of Deci-Binary Numbers](https://leetcode.com/problems/partitioning-into-minimum-number-of-deci-binary-numbers/) | Medium |  | [Java](partitioning-into-minimum-number-of-deci-binary-numbers/src/Main.java) |
<!-- SOLUTIONS-END -->

## Decision Framework

Before solving any problem, ask yourself:

> "If I add 1 element to the window/search space, is the result **guaranteed** to move in one direction?"

| Answer | Meaning | Use |
|--------|---------|-----|
| **Yes, always consistent** | Monotonic | Sliding Window, Binary Search, Two Pointers |
| **No, can go either way** | Non-Monotonic | Prefix Sum + HashMap, DP, Backtracking |

## Project Structure

```
train-leet-code/
├── hooks/
│   └── pre-commit           # Auto-updates README.md & studyplan.md on commit
├── problem-name/
│   └── src/
│       └── Main.java        # Solution + test cases
├── fetch-leetcode.py         # Fetch problem details from LeetCode API
├── new-problem.sh            # Scaffold a new problem directory
├── post-to-leetcode.py       # Post solution article to LeetCode Solutions tab
├── submit-to-leetcode.py     # Submit solution code to LeetCode (like clicking Submit)
├── update-progress.py        # Progress tracker (called by pre-commit hook)
├── gpush                     # git push + auto-generate & post solution article
└── studyplan.md              # Full 19-week study plan
```

## Getting Started

```bash
# After cloning, run setup
git config core.hooksPath hooks/
git config alias.push-lc '!./gpush'
git config alias.submit-lc '!./submit-to-leetcode.py'

# Set up LeetCode credentials
cp .env.example .env
# Edit .env and fill in LEETCODE_SESSION and LEETCODE_CSRFTOKEN
# (get these from browser DevTools → Application → Cookies → leetcode.com)

# Create a new problem
./new-problem.sh <problem-name>

# Run a solution locally
cd <problem-name>
javac src/Main.java -d out && java -cp out Main

# Submit solution to LeetCode
git submit-lc <problem-name>   # from repo root
git submit-lc                  # from inside problem folder

# Push + auto-post solution article
git push-lc
```

## Study Plan

The full study plan covers **11 phases across 19 weeks**, progressing from pattern recognition to advanced data structures. See [`studyplan.md`](studyplan.md) for the complete roadmap.

## Author

**Jonathan Laksamana Purnomo** — [GitHub](https://github.com/jonatanlaksamanapurnomo)
