#!/usr/bin/env python3
"""Submit a solution to LeetCode (like clicking the Submit button)."""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def load_env():
    """Load credentials from .env file."""
    env_path = os.path.join(REPO_ROOT, ".env")
    env = {}
    if not os.path.exists(env_path):
        print("ERROR: .env file not found. Copy .env.example to .env and fill in your credentials.", file=sys.stderr)
        sys.exit(1)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip()
    return env


def get_headers(session, csrf):
    """Build request headers with auth cookies."""
    return {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={session}; csrftoken={csrf}",
        "x-csrftoken": csrf,
        "Referer": "https://leetcode.com/",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://leetcode.com",
    }


def fetch_question_id(slug, headers):
    """Fetch the numeric question ID from LeetCode GraphQL API."""
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
        }
    }
    """
    payload = json.dumps({
        "query": query,
        "variables": {"titleSlug": slug},
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://leetcode.com/graphql/",
        data=payload,
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["data"]["question"]["questionId"]


def extract_solution_code(java_path):
    """Extract the Solution class (with imports) from Main.java."""
    with open(java_path) as f:
        content = f.read()

    lines = content.split("\n")
    result_lines = []
    in_solution = False
    brace_depth = 0

    for line in lines:
        # Skip comment header lines
        if line.startswith("//"):
            continue

        # Collect import statements
        if line.startswith("import "):
            result_lines.append(line)
            continue

        # Start of Solution class
        if re.match(r'^class Solution', line):
            in_solution = True

        if in_solution:
            result_lines.append(line)
            brace_depth += line.count("{") - line.count("}")
            if brace_depth == 0 and "{" in line or (brace_depth == 0 and "}" in line):
                if brace_depth == 0 and result_lines:
                    # Check if we've closed the Solution class
                    break

    return "\n".join(result_lines).strip()


def extract_slug_from_java(java_path):
    """Extract problem slug from the URL comment in Main.java."""
    with open(java_path) as f:
        for line in f:
            m = re.search(r'leetcode\.com/problems/([^/\s]+)', line)
            if m:
                return m.group(1)
    return None


def submit_solution(slug, typed_code, question_id, headers):
    """Submit solution to LeetCode and return submission ID."""
    payload = json.dumps({
        "lang": "java",
        "question_id": question_id,
        "typed_code": typed_code,
    }).encode("utf-8")

    headers = dict(headers)
    headers["Referer"] = f"https://leetcode.com/problems/{slug}/submissions/"

    req = urllib.request.Request(
        f"https://leetcode.com/problems/{slug}/submit/",
        data=payload,
        headers=headers,
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    submission_id = data.get("submission_id")
    if not submission_id:
        print(f"ERROR: No submission_id returned. Response: {json.dumps(data, indent=2)}", file=sys.stderr)
        sys.exit(1)

    return submission_id


def check_submission(submission_id, headers):
    """Poll submission status until it's done."""
    url = f"https://leetcode.com/submissions/detail/{submission_id}/check/"
    headers = dict(headers)
    headers.pop("Content-Type", None)

    max_attempts = 30
    for attempt in range(max_attempts):
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        state = data.get("state")
        if state == "SUCCESS":
            return data
        if state == "PENDING" or state == "STARTED":
            time.sleep(1)
            continue
        # Unknown state — return whatever we got
        return data

    print("ERROR: Submission check timed out after 30 seconds.", file=sys.stderr)
    sys.exit(1)


def format_result(result):
    """Format submission result for display."""
    status = result.get("status_msg", "Unknown")
    lines = []

    if status == "Accepted":
        lines.append("\033[32m✓ Accepted\033[0m")
        runtime = result.get("status_runtime", "?")
        memory = result.get("status_memory", "?")
        runtime_pct = result.get("runtime_percentile", "")
        memory_pct = result.get("memory_percentile", "")

        rt_str = f"  Runtime: {runtime}"
        if runtime_pct:
            rt_str += f" (beats {runtime_pct:.1f}%)"
        lines.append(rt_str)

        mem_str = f"  Memory:  {memory}"
        if memory_pct:
            mem_str += f" (beats {memory_pct:.1f}%)"
        lines.append(mem_str)

        total = result.get("total_testcases", "?")
        lines.append(f"  Tests:   {total}/{total} passed")
    else:
        lines.append(f"\033[31m✗ {status}\033[0m")

        if status == "Wrong Answer":
            total = result.get("total_testcases", "?")
            correct = result.get("total_correct", "?")
            lines.append(f"  Tests: {correct}/{total} passed")
            inp = result.get("input_formatted", result.get("input", ""))
            expected = result.get("expected_output", "")
            actual = result.get("code_output", "")
            if inp:
                lines.append(f"  Input:    {_truncate(inp, 100)}")
            if expected:
                lines.append(f"  Expected: {_truncate(expected, 100)}")
            if actual:
                lines.append(f"  Output:   {_truncate(actual, 100)}")

        elif status == "Time Limit Exceeded":
            total = result.get("total_testcases", "?")
            correct = result.get("total_correct", "?")
            lines.append(f"  Tests: {correct}/{total} passed before TLE")

        elif status == "Runtime Error":
            err = result.get("runtime_error", result.get("full_runtime_error", ""))
            if err:
                lines.append(f"  Error: {_truncate(err, 200)}")

        elif status == "Compile Error":
            err = result.get("compile_error", result.get("full_compile_error", ""))
            if err:
                lines.append(f"  Error: {_truncate(err, 200)}")

    return "\n".join(lines)


def _truncate(s, max_len):
    """Truncate string with ellipsis."""
    s = s.replace("\n", " ").strip()
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


def resolve_slug(arg):
    """Resolve the slug and java file path from the argument.

    Accepts:
      - A problem slug (e.g., "two-sum")
      - A path to Main.java
      - No argument (uses current directory name as slug)
    """
    if arg:
        # Check if it's a file path
        if arg.endswith(".java") and os.path.isfile(arg):
            slug = extract_slug_from_java(arg)
            return slug, arg
        # Check if it's a directory
        if os.path.isdir(os.path.join(REPO_ROOT, arg, "src")):
            java_path = os.path.join(REPO_ROOT, arg, "src", "Main.java")
            slug = arg
            return slug, java_path
        # Treat as slug
        java_path = os.path.join(REPO_ROOT, arg, "src", "Main.java")
        return arg, java_path
    else:
        # Use current directory
        cwd = os.getcwd()
        dirname = os.path.basename(cwd)
        # Check if we're in the problem directory
        java_path = os.path.join(cwd, "src", "Main.java")
        if os.path.isfile(java_path):
            slug = extract_slug_from_java(java_path) or dirname
            return slug, java_path
        # Check if we're in src/
        java_path = os.path.join(cwd, "Main.java")
        if os.path.isfile(java_path):
            slug = extract_slug_from_java(java_path) or os.path.basename(os.path.dirname(cwd))
            return slug, java_path
        # Check from repo root
        print("ERROR: Could not find Main.java. Run from a problem directory or pass the slug as argument.", file=sys.stderr)
        print("Usage: submit-to-leetcode.py [slug]", file=sys.stderr)
        sys.exit(1)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    slug, java_path = resolve_slug(arg)

    if not os.path.isfile(java_path):
        print(f"ERROR: File not found: {java_path}", file=sys.stderr)
        sys.exit(1)

    # Load credentials
    env = load_env()
    session = env.get("LEETCODE_SESSION", "")
    csrf = env.get("LEETCODE_CSRFTOKEN", "")
    if not session or not csrf:
        print("ERROR: LEETCODE_SESSION and LEETCODE_CSRFTOKEN must be set in .env", file=sys.stderr)
        sys.exit(1)

    headers = get_headers(session, csrf)

    # Extract solution code
    typed_code = extract_solution_code(java_path)
    if not typed_code:
        print("ERROR: Could not extract Solution class from Main.java", file=sys.stderr)
        sys.exit(1)

    # Get question ID
    print(f"Submitting: {slug}")
    question_id = fetch_question_id(slug, headers)

    # Submit
    print("Sending submission...")
    submission_id = submit_solution(slug, typed_code, question_id, headers)
    print(f"Submission ID: {submission_id}")

    # Poll for result
    print("Waiting for result...\n")
    result = check_submission(submission_id, headers)

    # Display result
    print(format_result(result))


if __name__ == "__main__":
    main()
