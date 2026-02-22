#!/usr/bin/env python3
"""Auto-update README.md and studyplan.md based on solution directories."""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
STUDYPLAN = os.path.join(ROOT, "studyplan.md")
README = os.path.join(ROOT, "README.md")
PROBLEM_CACHE = os.path.join(ROOT, ".problem-cache.json")

# Priority-ordered: first match wins
TOPIC_TAG_TO_PATTERN = [
    ("Sliding Window", "Sliding Window"),
    ("Prefix Sum", "Prefix Sum"),
    ("Two Pointers", "Two Pointers"),
    ("Monotonic Stack", "Monotonic Stack"),
    ("Binary Search", "Binary Search"),
    ("Dynamic Programming", "DP"),
    ("Graph", "Graph"),
    ("Tree", "Tree"),
    ("Backtracking", "Backtracking"),
    ("Heap (Priority Queue)", "Heap"),
    ("Union Find", "Union Find"),
    ("Trie", "Trie"),
    ("Bit Manipulation", "Bit Manipulation"),
    ("Math", "Math"),
]

PHASE_LABELS = {
    1: "Sliding Window",
    2: "Prefix Sum + HashMap",
    3: "Two Pointers",
    4: "Monotonic Stack",
    5: "Binary Search",
    6: "Dynamic Programming",
    7: "Graph (BFS/DFS)",
    8: "Tree",
    9: "Backtracking",
    10: "Heap / Priority Queue",
    11: "Advanced (UF/Trie)",
}


def find_solutions():
    """Scan for solved problems. Returns dict url_slug -> info."""
    solutions = {}
    for entry in sorted(os.listdir(ROOT)):
        main_java = os.path.join(ROOT, entry, "src", "Main.java")
        if not os.path.isfile(main_java):
            continue
        with open(main_java) as f:
            file_lines = f.readlines()
        if len(file_lines) < 2:
            continue
        m1 = re.match(r"^//\s*(\d+)\.\s*(.+)$", file_lines[0].strip())
        m2 = re.match(
            r"^//\s*(https://leetcode\.com/problems/([^/]+)/?)", file_lines[1].strip()
        )
        if m1 and m2:
            solutions[m2.group(2)] = {
                "number": int(m1.group(1)),
                "title": m1.group(2).strip(),
                "url": m2.group(1),
                "slug": m2.group(2),
                "dir": entry,
            }
    return solutions


def title_to_slug(title):
    """Convert problem title to LeetCode-style slug."""
    s = title.lower()
    s = s.replace("\u2014", "-").replace("\u2013", "-")  # em-dash, en-dash
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s-]+", "-", s)
    return s.strip("-")


def _phase_to_pattern(phase, sub):
    mapping = {
        1: "Sliding Window",
        2: "Prefix Sum",
        3: "Two Pointers",
        4: "Monotonic Stack",
        5: "Binary Search",
        6: "DP",
        7: "Graph",
        8: "Tree",
        9: "Backtracking",
        10: "Heap",
    }
    if phase == 11:
        sub_l = (sub or "").lower()
        if "union" in sub_l:
            return "Union Find"
        if "trie" in sub_l:
            return "Trie"
        return "Bit Manipulation"
    return mapping.get(phase, "")


def tags_to_pattern(topic_tags):
    """Pick the most relevant pattern from LeetCode topic tags."""
    tag_names = {t["name"] for t in topic_tags}
    for tag, pattern in TOPIC_TAG_TO_PATTERN:
        if tag in tag_names:
            return pattern
    return ""


def load_cache():
    """Load problem metadata cache from disk."""
    if os.path.isfile(PROBLEM_CACHE):
        with open(PROBLEM_CACHE) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    """Write problem metadata cache to disk."""
    with open(PROBLEM_CACHE, "w") as f:
        json.dump(cache, f, indent=2, sort_keys=True)
        f.write("\n")


def resolve_metadata(solutions):
    """Resolve difficulty + pattern for each solution via cache or LeetCode API.

    Returns dict slug -> {difficulty, pattern, topicTags}.
    """
    # Import fetch_metadata from fetch-leetcode.py
    sys.path.insert(0, ROOT)
    from importlib import import_module
    fetch_mod = import_module("fetch-leetcode")
    fetch_metadata = fetch_mod.fetch_metadata

    cache = load_cache()
    problem_meta = {}
    fetched = 0

    for slug in solutions:
        if slug in cache:
            problem_meta[slug] = cache[slug]
            continue

        # Fetch from API
        try:
            q = fetch_metadata(slug)
            topic_tags = q.get("topicTags", [])
            entry = {
                "difficulty": q.get("difficulty", ""),
                "pattern": tags_to_pattern(topic_tags),
                "topicTags": [t["name"] for t in topic_tags],
            }
            cache[slug] = entry
            problem_meta[slug] = entry
            fetched += 1
            print(f"  Fetched: {slug}")
        except Exception as e:
            print(f"  Warning: could not fetch {slug}: {e}", file=sys.stderr)
            problem_meta[slug] = {"difficulty": "", "pattern": "", "topicTags": []}

    if fetched > 0:
        save_cache(cache)
        print(f"  Cached {fetched} new problem(s)")

    return problem_meta


def update_studyplan(solutions):
    """Update studyplan.md checkboxes and progress tracker.

    Returns:
        sp_meta: dict slug -> {number, title, difficulty, pattern}
        phase_counts: dict phase_num -> (solved, total)
        total_solved: int
        total_all: int
    """
    with open(STUDYPLAN) as f:
        lines = f.readlines()

    solved_slugs = set(solutions.keys())
    sp_meta = {}

    current_phase = 0
    current_week = 0
    current_sub = ""

    phase_weeks = {}  # phase_num -> [week_nums]
    week_data = {}  # week_num -> [(slug, solved_bool)]

    # Pass 1: update checkboxes and collect metadata
    for i, line in enumerate(lines):
        pm = re.match(r"^## Phase (\d+):", line)
        if pm:
            current_phase = int(pm.group(1))

        wm = re.match(r"^### Week (\d+):\s*(.+)$", line)
        if wm:
            current_week = int(wm.group(1))
            current_sub = wm.group(2).strip()
            phase_weeks.setdefault(current_phase, []).append(current_week)
            week_data[current_week] = []

        prob_m = re.match(
            r"^- \[[ x]\] \*\*(\d+)\.\s*(.+?)\*\*\s*\((\w+)\)", line
        )
        if prob_m:
            number = int(prob_m.group(1))
            title = prob_m.group(2).strip()
            difficulty = prob_m.group(3)
            slug = title_to_slug(title)
            pattern = _phase_to_pattern(current_phase, current_sub)

            is_solved = slug in solved_slugs

            sp_meta[slug] = {
                "number": number,
                "title": title,
                "difficulty": difficulty,
                "pattern": pattern,
            }

            if is_solved:
                lines[i] = lines[i].replace("- [ ]", "- [x]", 1)
            else:
                lines[i] = lines[i].replace("- [x]", "- [ ]", 1)

            if current_week in week_data:
                week_data[current_week].append((slug, is_solved))

    # Pass 2: update progress tracker rows (ordered by week number)
    tracker_idx = 0
    weeks_sorted = sorted(week_data.keys())
    total_solved = 0
    total_all = 0

    for i, line in enumerate(lines):
        tm = re.match(
            r"^(\|\s*\d+\s*\|[^|]+\|)\s*\d+\s*\|\s*\d*/\d+\s*\|", line
        )
        if tm:
            if tracker_idx < len(weeks_sorted):
                wk = weeks_sorted[tracker_idx]
                probs = week_data[wk]
                solved = sum(1 for _, s in probs if s)
                total = len(probs)
                total_solved += solved
                total_all += total
                lines[i] = f"{tm.group(1)} {total} | {solved}/{total} |\n"
                tracker_idx += 1

        if line.startswith("| **Total**"):
            lines[i] = (
                f"| **Total** | | **{total_all}** | **{total_solved}/{total_all}** |\n"
            )

    with open(STUDYPLAN, "w") as f:
        f.writelines(lines)

    # Compute phase-level counts for README progress bars
    phase_counts = {}
    for pnum in sorted(phase_weeks.keys()):
        s, t = 0, 0
        for wk in phase_weeks[pnum]:
            probs = week_data.get(wk, [])
            s += sum(1 for _, sv in probs if sv)
            t += len(probs)
        phase_counts[pnum] = (s, t)

    return sp_meta, phase_counts, total_solved, total_all


def make_progress_bar(solved, total, width=10):
    if total == 0:
        return "\u2591" * width
    filled = round(solved / total * width)
    return "\u2588" * filled + "\u2591" * (width - filled)


def _generate_progress_block(solutions, phase_counts, total_all):
    """Generate the progress section content (between markers)."""
    lines = []
    lines.append(f"## Progress: {len(solutions)} / {total_all} solved\n")
    lines.append("\n")
    lines.append("```\n")
    for pnum in sorted(PHASE_LABELS.keys()):
        label = PHASE_LABELS[pnum]
        s, t = phase_counts.get(pnum, (0, 0))
        bar = make_progress_bar(s, t)
        lines.append(f"Phase {pnum:<2} {label:<22}{bar}  {s}/{t}\n")
    lines.append("```\n")
    return lines


def _generate_solutions_block(solutions, problem_meta):
    """Generate the solutions table content (between markers)."""
    lines = []
    lines.append("## Solutions\n")
    lines.append("\n")
    lines.append("| # | Problem | Difficulty | Pattern | Solution |\n")
    lines.append("|---|---------|------------|---------|----------|\n")
    entries = []
    for slug, sol in solutions.items():
        meta = problem_meta.get(slug, {})
        entries.append(
            {
                "number": sol["number"],
                "title": sol["title"],
                "url": sol["url"],
                "difficulty": meta.get("difficulty", ""),
                "pattern": meta.get("pattern", ""),
                "dir": sol["dir"],
            }
        )
    entries.sort(key=lambda e: e["number"])
    for e in entries:
        lines.append(
            f"| {e['number']} | [{e['title']}]({e['url']}) "
            f"| {e['difficulty']} | {e['pattern']} "
            f"| [Java]({e['dir']}/src/Main.java) |\n"
        )
    return lines


def update_readme(solutions, problem_meta, phase_counts, total_solved, total_all):
    """Update README.md progress section and solutions table.

    Only content between <!-- PROGRESS-START/END --> and
    <!-- SOLUTIONS-START/END --> markers is replaced.
    Everything else is preserved exactly as-is.
    """
    with open(README) as f:
        content = f.read()

    PROG_START = "<!-- PROGRESS-START -->"
    PROG_END = "<!-- PROGRESS-END -->"
    SOL_START = "<!-- SOLUTIONS-START -->"
    SOL_END = "<!-- SOLUTIONS-END -->"

    # Replace progress section
    ps = content.find(PROG_START)
    pe = content.find(PROG_END)
    if ps != -1 and pe != -1:
        new_progress = "".join(_generate_progress_block(solutions, phase_counts, total_all))
        content = (
            content[: ps + len(PROG_START)]
            + "\n"
            + new_progress
            + content[pe:]
        )

    # Replace solutions section
    ss = content.find(SOL_START)
    se = content.find(SOL_END)
    if ss != -1 and se != -1:
        new_solutions = "".join(_generate_solutions_block(solutions, problem_meta))
        content = (
            content[: ss + len(SOL_START)]
            + "\n"
            + new_solutions
            + content[se:]
        )

    with open(README, "w") as f:
        f.write(content)


def main():
    solutions = find_solutions()
    problem_meta = resolve_metadata(solutions)
    sp_meta, phase_counts, total_solved, total_all = update_studyplan(solutions)
    update_readme(solutions, problem_meta, phase_counts, total_solved, total_all)
    print(
        f"Updated: {total_solved}/{total_all} studyplan problems solved, "
        f"{len(solutions)} total solutions"
    )


if __name__ == "__main__":
    main()
