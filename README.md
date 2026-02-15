# LeetCode Training

My journey solving 81 LeetCode problems, organized by pattern and topic — not by difficulty.

> **Philosophy:** Understand *why* an approach works, not memorize solutions.
> For every problem, ask: "Is it monotonic or not? Why?"

## Progress: 6 / 81 solved

```
Phase 1  Sliding Window        ██████░░░░  5/9
Phase 2  Prefix Sum + HashMap  ░░░░░░░░░░  0/7
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

## Solutions

| # | Problem | Difficulty | Pattern | Solution |
|---|---------|------------|---------|----------|
| 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Sliding Window | [Java](longest-substring-without-repeating-characters/src/Main.java) |
| 67 | [Add Binary](https://leetcode.com/problems/add-binary/) | Easy | Bit Manipulation | [Java](add-binary/src/Main.java) |
| 209 | [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | Sliding Window | [Java](minimum-size-subarray-sum/src/Main.java) |
| 643 | [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | Easy | Sliding Window | [Java](maximum-average-subarray-i/src/Main.java) |
| 1046 | [Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | Medium | Sliding Window | [Java](max-consecutive-ones-iii/src/Main.java) |
| 1567 | [Maximum Number of Vowels in a Substring of Given Length](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) | Medium | Sliding Window | [Java](maximum-number-of-vowels-in-a-substring-of-given-length/src/Main.java) |

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
├── problem-name/
│   └── src/
│       └── Main.java        # Solution + test cases
├── fetch-leetcode.py         # Fetch problem details from LeetCode API
├── new-problem.sh            # Scaffold a new problem directory
└── studyplan.md              # Full 19-week study plan
```

## Getting Started

```bash
# Create a new problem
./new-problem.sh <problem-name>

# Run a solution
cd <problem-name>
javac src/Main.java -d out && java -cp out Main
```

## Study Plan

The full study plan covers **11 phases across 19 weeks**, progressing from pattern recognition to advanced data structures. See [`studyplan.md`](studyplan.md) for the complete roadmap.

## Author

**Jonathan Laksamana Purnomo** — [GitHub](https://github.com/jonatanlaksamanapurnomo)
