#!/usr/bin/env python3
"""Auto-update README.md and studyplan.md based on solution directories."""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
STUDYPLAN = os.path.join(ROOT, "studyplan.md")
README = os.path.join(ROOT, "README.md")

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


def parse_readme_table():
    """Parse existing README solutions table for non-studyplan problem metadata."""
    existing = {}
    with open(README) as f:
        for line in f:
            m = re.match(
                r"^\|\s*(\d+)\s*\|[^|]+\|\s*(\w*)\s*\|\s*([^|]*)\s*\|", line
            )
            if m:
                existing[int(m.group(1))] = {
                    "difficulty": m.group(2).strip(),
                    "pattern": m.group(3).strip(),
                }
    return existing


def update_readme(solutions, sp_meta, phase_counts, total_solved, total_all):
    """Update README.md progress section and solutions table."""
    existing_table = parse_readme_table()

    with open(README) as f:
        lines = f.readlines()

    new_lines = []
    state = "normal"
    progress_block_done = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # --- State: skipping old progress bar lines ---
        if state == "skip_progress_bars":
            if line.strip() == "```":
                # Write new bars then closing ```
                for pnum in sorted(PHASE_LABELS.keys()):
                    label = PHASE_LABELS[pnum]
                    s, t = phase_counts.get(pnum, (0, 0))
                    bar = make_progress_bar(s, t)
                    new_lines.append(
                        f"Phase {pnum:<2} {label:<22}{bar}  {s}/{t}\n"
                    )
                new_lines.append("```\n")
                state = "normal"
            i += 1
            continue

        # --- State: skipping old solutions table rows ---
        if state == "skip_table":
            if line.startswith("|"):
                i += 1
                continue
            state = "normal"
            # Fall through to process this line normally

        # --- Normal state ---
        # Update progress header
        if line.startswith("## Progress:"):
            new_lines.append(
                f"## Progress: {len(solutions)} / {total_all} solved\n"
            )
            i += 1
            continue

        # Detect progress bars code block
        if (
            line.strip() == "```"
            and not progress_block_done
            and any(
                "Progress" in lines[j] for j in range(max(0, i - 3), i)
            )
        ):
            new_lines.append("```\n")
            progress_block_done = True
            state = "skip_progress_bars"
            i += 1
            continue

        # Replace solutions table
        if line.startswith("## Solutions"):
            new_lines.append(line)
            i += 1
            # Preserve blank line after heading
            if i < len(lines) and lines[i].strip() == "":
                new_lines.append(lines[i])
                i += 1
            # Write new table
            new_lines.append(
                "| # | Problem | Difficulty | Pattern | Solution |\n"
            )
            new_lines.append(
                "|---|---------|------------|---------|----------|\n"
            )
            entries = []
            for slug, sol in solutions.items():
                meta = sp_meta.get(slug, {})
                number = meta.get("number", sol["number"])
                title = meta.get("title", sol["title"])
                difficulty = meta.get("difficulty", "")
                pattern = meta.get("pattern", "")
                # Fallback to existing README data for non-studyplan problems
                if not difficulty and number in existing_table:
                    difficulty = existing_table[number].get("difficulty", "")
                if not pattern and number in existing_table:
                    pattern = existing_table[number].get("pattern", "")
                entries.append(
                    {
                        "number": number,
                        "title": title,
                        "url": sol["url"],
                        "difficulty": difficulty,
                        "pattern": pattern,
                        "dir": sol["dir"],
                    }
                )
            entries.sort(key=lambda e: e["number"])
            for e in entries:
                new_lines.append(
                    f"| {e['number']} | [{e['title']}]({e['url']}) "
                    f"| {e['difficulty']} | {e['pattern']} "
                    f"| [Java]({e['dir']}/src/Main.java) |\n"
                )
            state = "skip_table"
            continue

        new_lines.append(line)
        i += 1

    with open(README, "w") as f:
        f.writelines(new_lines)


def main():
    solutions = find_solutions()
    sp_meta, phase_counts, total_solved, total_all = update_studyplan(solutions)
    update_readme(solutions, sp_meta, phase_counts, total_solved, total_all)
    print(
        f"Updated: {total_solved}/{total_all} studyplan problems solved, "
        f"{len(solutions)} total solutions"
    )


if __name__ == "__main__":
    main()
