# LeetCode Study Plan: From Monotonic Thinking to Complete DSA Mastery

> **Filosofi:** Pahami *kenapa* sebuah approach works, bukan hafal solusi.
> Untuk setiap soal, tanyakan: "Monotonic atau tidak? Kenapa?"

---

## 🔑 Decision Framework

Sebelum solve soal apapun, tanyakan ke diri sendiri:

> "Kalau saya tambah 1 elemen ke window/search space, apakah hasilnya **pasti** makin memenuhi atau **pasti** makin tidak memenuhi?"

| Jawaban | Artinya | Pattern yang Bisa Dipakai |
|---------|---------|--------------------------|
| **Ya, pasti konsisten** | Monotonic | Sliding Window, Binary Search, Two Pointers, Monotonic Stack |
| **Tidak, bisa bolak-balik** | Non-Monotonic | Prefix Sum + HashMap, DP, Divide & Conquer |

---

## Phase 1: Foundation — Sliding Window (Monotonic)

Pahami dulu kapan dan kenapa sliding window works.

### Week 1: Basic Sliding Window (Fixed Size)

**Konsep:** Window fixed size, geser dari kiri ke kanan. Tidak perlu shrink/expand — cukup slide.

- [x] **643. Maximum Average Subarray I** (Easy) — window fixed size, cari max average
- [x] **1456. Maximum Number of Vowels in a Substring of Given Length** (Medium) — sama tapi track vowel count
- [x] **219. Contains Duplicate II** (Easy) — window fixed size, cek duplikat

> **Pertanyaan setelah solve:**
> - "Kenapa saya tidak perlu cek semua kemungkinan subarray?"
> - "Apa yang berubah setiap kali window geser 1 langkah?"

### Week 2: Dynamic Sliding Window (Shrink/Expand)

**Konsep:** Window size berubah-ubah, kamu tentukan kapan shrink berdasarkan sifat monotonic.

- [x] **209. Minimum Size Subarray Sum** (Medium) — expand → sum pasti naik, shrink → sum pasti turun
- [x] **3. Longest Substring Without Repeating Characters** (Medium) — expand → duplikat hanya bisa bertambah
- [x] **1004. Max Consecutive Ones III** (Medium) — expand → jumlah 0 hanya bisa bertambah
- [x] **904. Fruit Into Baskets** (Medium) — paling banyak 2 jenis buah di window
- [x] **424. Longest Repeating Character Replacement** (Medium) — tricky, pikirkan kenapa monotonic
- [ ] **1358. Number of Substrings Containing All Three Characters** (Medium) — shrink saat sudah punya semua 3 karakter

> **Pertanyaan setelah solve:**
> - "Apa kondisi yang membuat saya harus shrink?"
> - "Kenapa shrink **pasti** mengarah ke solusi yang benar?"
> - "Apakah ada kemungkinan saya melewatkan jawaban optimal dengan shrink?"

---

## Phase 2: Prefix Sum + HashMap (Non-Monotonic)

Pahami kenapa sliding window gagal di sini, dan kenapa prefix works.

### Week 3: Basic Prefix Sum

**Konsep:** Kalau expand/shrink tidak predictable, jangan pakai window. Track state di setiap posisi, cari posisi sebelumnya yang punya state sama.

**Prinsip inti:** Jika `prefix[j] - prefix[i] = target`, maka subarray `i+1..j` punya sum = target.

- [ ] **560. Subarray Sum Equals K** (Medium) — klasik prefix sum + hashmap
- [ ] **974. Subarray Sums Divisible by K** (Medium) — prefix sum + modulo trick
- [ ] **525. Contiguous Array** (Medium) — 0 dan 1 sama jumlahnya → track selisih count

> **Pertanyaan setelah solve:**
> - "Kenapa sliding window tidak bisa di sini?"
> - "Coba expand window — apakah hasilnya predictable?"
> - "Apa yang disimpan di hashmap, dan kenapa itu cukup?"

### Week 4: Advanced Prefix

- [ ] **930. Binary Subarrays With Sum** (Medium) — count subarray dengan sum tertentu
- [ ] **1248. Count Number of Nice Subarrays** (Medium) — mirip tapi count odd numbers
- [ ] **3714. Longest Balanced Substring II** (Medium) — track selisih antar count karakter
- [ ] **1371. Find the Longest Substring Containing Vowels in Even Counts** (Medium) — prefix + bitmask

> **Pertanyaan setelah solve:**
> - "Kenapa menyimpan selisih/state di hashmap bisa menggantikan pengecekan semua subarray?"
> - "Kapan saya simpan index pertama vs kapan saya simpan count?"

---

## Phase 3: Two Pointers (Monotonic)

Variasi lain dari monotonic thinking — dua pointer yang bergerak berdasarkan kondisi yang predictable.

### Week 5: Sorted Array Two Pointers

**Konsep:** Di sorted array, geser kiri → nilai naik, geser kanan → nilai turun. Predictable.

- [ ] **167. Two Sum II — Input Array Is Sorted** (Medium) — sum terlalu besar → geser kanan, terlalu kecil → geser kiri
- [ ] **15. 3Sum** (Medium) — fix satu elemen, two pointer untuk sisanya
- [ ] **11. Container With Most Water** (Medium) — kenapa selalu geser yang lebih pendek
- [ ] **42. Trapping Rain Water** (Hard) — two pointer dari kedua ujung

> **Pertanyaan setelah solve:**
> - "Kenapa saya bisa yakin menggeser pointer ini tidak akan melewatkan jawaban?"
> - "Apa invariant yang dipertahankan setiap langkah?"

---

## Phase 4: Monotonic Stack

### Week 6: Stack yang Selalu Terurut

**Konsep:** Maintain stack yang isinya selalu naik atau turun. Saat elemen baru melanggar urutan, pop — dan setiap pop memberikan informasi berguna.

- [ ] **496. Next Greater Element I** (Easy) — intro monotonic stack
- [ ] **739. Daily Temperatures** (Medium) — berapa hari sampai lebih hangat
- [ ] **503. Next Greater Element II** (Medium) — circular array
- [ ] **84. Largest Rectangle in Histogram** (Hard) — klasik, setiap pop hitung area

> **Pertanyaan setelah solve:**
> - "Kenapa saya bisa pop dari stack tanpa kehilangan informasi penting?"
> - "Apa yang direpresentasikan oleh stack pada setiap saat?"

---

## Phase 5: Binary Search (Monotonic)

### Week 7: Search Space yang Monotonic

**Konsep:** Jika f(x) monotonic (kalau x naik, f(x) juga konsisten naik/turun), kamu bisa binary search.

- [ ] **704. Binary Search** (Easy) — dasar
- [ ] **35. Search Insert Position** (Easy) — variasi boundary
- [ ] **875. Koko Eating Bananas** (Medium) — binary search on answer: speed naik → waktu pasti turun
- [ ] **1011. Capacity To Ship Packages Within D Days** (Medium) — kapasitas naik → hari pasti turun
- [ ] **153. Find Minimum in Rotated Sorted Array** (Medium) — partially sorted, masih monotonic per segment

> **Pertanyaan setelah solve:**
> - "Kenapa kalau mid tidak valid, saya bisa buang setengah search space?"
> - "Apa yang monotonic di sini — input atau search space?"

---

## Phase 6: Dynamic Programming

**Ini yang paling penting setelah monotonic patterns. ~30-40% soal medium/hard butuh DP.**

### Week 8: DP Basics — 1D

**Konsep:** Pecah masalah besar jadi subproblem kecil. Simpan hasil subproblem supaya tidak hitung ulang.

- [ ] **70. Climbing Stairs** (Easy) — intro DP, mirip fibonacci
- [ ] **198. House Robber** (Medium) — pilih atau skip, carry forward max
- [ ] **213. House Robber II** (Medium) — circular variant
- [ ] **322. Coin Change** (Medium) — unbounded knapsack classic
- [ ] **300. Longest Increasing Subsequence** (Medium) — classic LIS

> **Pertanyaan setelah solve:**
> - "Apa subproblem-nya? Apa yang di-cache?"
> - "Apakah bisa solve ini tanpa DP? Kenapa DP lebih baik?"
> - "Bottom-up atau top-down — mana yang lebih natural untuk soal ini?"

### Week 9: DP Basics — 2D

**Konsep:** State butuh 2 dimensi — biasanya index di dua sequence, atau posisi di grid.

- [ ] **62. Unique Paths** (Medium) — grid DP dasar
- [ ] **64. Minimum Path Sum** (Medium) — grid + optimization
- [ ] **1143. Longest Common Subsequence** (Medium) — 2 string, classic
- [ ] **72. Edit Distance** (Hard) — 2 string, 3 operasi
- [ ] **518. Coin Change II** (Medium) — count combinations, beda dari coin change I

> **Pertanyaan setelah solve:**
> - "Kenapa butuh 2 dimensi? Apa arti setiap dimensi?"
> - "Bisa dioptimasi space-nya dari 2D ke 1D?"

### Week 10: DP Patterns — Knapsack & Intervals

**Konsep:** Pattern DP yang sering muncul.

- [ ] **416. Partition Equal Subset Sum** (Medium) — 0/1 knapsack
- [ ] **494. Target Sum** (Medium) — variasi knapsack dengan +/-
- [ ] **139. Word Break** (Medium) — string DP
- [ ] **152. Maximum Product Subarray** (Medium) — track min dan max
- [ ] **647. Palindromic Substrings** (Medium) — expand around center atau DP

> **Pertanyaan setelah solve:**
> - "Pattern knapsack mana yang dipakai — 0/1 atau unbounded?"
> - "Apakah ada greedy solution? Kenapa DP diperlukan?"

---

## Phase 7: Graph — BFS & DFS

### Week 11: Graph Basics

**Konsep:** Banyak soal bisa dimodelkan sebagai graph — grid, tree, dependencies.

- [ ] **200. Number of Islands** (Medium) — DFS/BFS di grid, intro graph traversal
- [ ] **733. Flood Fill** (Easy) — BFS/DFS sederhana
- [ ] **994. Rotting Oranges** (Medium) — multi-source BFS
- [ ] **207. Course Schedule** (Medium) — topological sort, detect cycle
- [ ] **210. Course Schedule II** (Medium) — topological sort, return order

> **Pertanyaan setelah solve:**
> - "Kapan pakai BFS vs DFS?"
> - "BFS → shortest path (unweighted). DFS → explore all paths. Benar?"

### Week 12: Shortest Path & Advanced Graph

- [ ] **743. Network Delay Time** (Medium) — Dijkstra intro
- [ ] **133. Clone Graph** (Medium) — deep copy with visited map
- [ ] **417. Pacific Atlantic Water Flow** (Medium) — reverse thinking BFS/DFS
- [ ] **785. Is Graph Bipartite?** (Medium) — BFS/DFS coloring

> **Pertanyaan setelah solve:**
> - "Kenapa Dijkstra works? Apa yang monotonic di Dijkstra?" (hint: jarak terpendek selalu naik)

---

## Phase 8: Tree

### Week 13: Tree Traversal & Recursion

**Konsep:** Tree = recursive structure. Kebanyakan soal tree diselesaikan dengan recursive thinking.

- [ ] **104. Maximum Depth of Binary Tree** (Easy) — intro tree recursion
- [ ] **226. Invert Binary Tree** (Easy) — transform tree
- [ ] **543. Diameter of Binary Tree** (Easy) — track global max di recursion
- [ ] **236. Lowest Common Ancestor of a Binary Tree** (Medium) — classic LCA
- [ ] **105. Construct Binary Tree from Preorder and Inorder Traversal** (Medium) — rebuild tree

> **Pertanyaan setelah solve:**
> - "Apa base case recursion-nya?"
> - "Info apa yang dikembalikan dari subtree ke parent?"

### Week 14: BST & Advanced Tree

- [ ] **98. Validate Binary Search Tree** (Medium) — BST property + range checking
- [ ] **230. Kth Smallest Element in a BST** (Medium) — inorder traversal
- [ ] **297. Serialize and Deserialize Binary Tree** (Hard) — encode/decode tree
- [ ] **124. Binary Tree Maximum Path Sum** (Hard) — track global max, tricky recursion

---

## Phase 9: Backtracking

### Week 15: Generate All Possibilities

**Konsep:** Coba semua kemungkinan secara systematic. Kalau sudah pasti salah, backtrack (prune).

- [ ] **46. Permutations** (Medium) — generate semua permutasi
- [ ] **78. Subsets** (Medium) — generate semua subset
- [ ] **39. Combination Sum** (Medium) — combinations dengan pengulangan
- [ ] **79. Word Search** (Medium) — backtrack di grid
- [ ] **51. N-Queens** (Hard) — classic backtracking

> **Pertanyaan setelah solve:**
> - "Di mana saya prune? Apa yang menghemat waktu?"
> - "Bedanya backtracking dengan brute force apa?"

---

## Phase 10: Heap / Priority Queue

### Week 16: Top-K & Merge Problems

**Konsep:** Butuh akses cepat ke elemen terbesar/terkecil? Pakai heap.

- [ ] **215. Kth Largest Element in an Array** (Medium) — min heap size k
- [ ] **347. Top K Frequent Elements** (Medium) — frequency + heap
- [ ] **23. Merge k Sorted Lists** (Hard) — min heap untuk merge
- [ ] **295. Find Median from Data Stream** (Hard) — two heaps (max + min)

> **Pertanyaan setelah solve:**
> - "Kenapa heap lebih baik dari sort di sini?"
> - "Min heap atau max heap — mana yang dipakai dan kenapa?"

---

## Phase 11: Advanced Topics

### Week 17: Union Find

- [ ] **547. Number of Provinces** (Medium) — intro union find
- [ ] **684. Redundant Connection** (Medium) — detect cycle dengan union find
- [ ] **128. Longest Consecutive Sequence** (Medium) — bisa union find atau hashset

### Week 18: Trie

- [ ] **208. Implement Trie (Prefix Tree)** (Medium) — build trie dari scratch
- [ ] **211. Design Add and Search Words Data Structure** (Medium) — trie + wildcard
- [ ] **212. Word Search II** (Hard) — trie + backtracking

### Week 19: Bit Manipulation & Math

- [ ] **136. Single Number** (Easy) — XOR trick
- [ ] **191. Number of 1 Bits** (Easy) — bit counting
- [ ] **371. Sum of Two Integers** (Medium) — bit manipulation arithmetic
- [ ] **204. Count Primes** (Medium) — Sieve of Eratosthenes

---

## 📋 Cara Belajar Setiap Soal

Untuk setiap soal, **jangan langsung code**. Ikuti flow ini:

1. **Baca soal** — pahami input, output, constraint
2. **Tanya: monotonic atau tidak?** — kalau expand/geser, apakah hasilnya predictable?
3. **Pilih pattern** — sliding window, prefix + hashmap, DP, graph, dll
4. **Dry run di kertas** — gambar contoh kecil, trace logic step by step
5. **Baru code** — implement dari pemahaman, bukan dari hafalan
6. **Setelah solve, tanya:**
    - "Kenapa approach ini works?"
    - "Approach lain kenapa tidak bisa / kurang optimal?"
    - "Apa yang monotonic / non-monotonic di soal ini?"

---

## 📊 Progress Tracker

| Phase | Topic | Soal | Selesai |
|-------|-------|------|---------|
| 1 | Sliding Window (Fixed) | 3 | 3/3 |
| 1 | Sliding Window (Dynamic) | 6 | 5/6 |
| 2 | Prefix Sum Basic | 3 | 0/3 |
| 2 | Prefix Sum Advanced | 4 | 0/4 |
| 3 | Two Pointers | 4 | 0/4 |
| 4 | Monotonic Stack | 4 | 0/4 |
| 5 | Binary Search | 5 | 0/5 |
| 6 | DP 1D | 5 | 0/5 |
| 6 | DP 2D | 5 | 0/5 |
| 6 | DP Patterns | 5 | 0/5 |
| 7 | Graph Basic | 5 | 0/5 |
| 7 | Graph Advanced | 4 | 0/4 |
| 8 | Tree Basic | 5 | 0/5 |
| 8 | Tree Advanced | 4 | 0/4 |
| 9 | Backtracking | 5 | 0/5 |
| 10 | Heap | 4 | 0/4 |
| 11 | Union Find | 3 | 0/3 |
| 11 | Trie | 3 | 0/3 |
| 11 | Bit & Math | 4 | 0/4 |
| **Total** | | **81** | **8/81** |

---

> **Remember:** Understanding > Speed > Memorization.
> Kalau kamu paham *kenapa*, kamu bisa solve soal yang belum pernah kamu lihat.