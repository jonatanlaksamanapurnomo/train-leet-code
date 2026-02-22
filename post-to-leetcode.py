#!/usr/bin/env python3
"""Post a solution to LeetCode's Solutions tab via GraphQL API."""

import json
import os
import sys
import urllib.request
import urllib.error


def load_env():
    """Load credentials from .env file."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
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


def post_solution(slug, title, content):
    """Post solution to LeetCode via GraphQL."""
    env = load_env()
    session = env.get("LEETCODE_SESSION", "")
    csrf = env.get("LEETCODE_CSRFTOKEN", "")

    if not session or not csrf:
        print("ERROR: LEETCODE_SESSION and LEETCODE_CSRFTOKEN must be set in .env", file=sys.stderr)
        sys.exit(1)

    # GraphQL mutation for publishing a solution article
    query = """
    mutation ugcArticlePublishSolution($data: UgcArticlePublishSolutionInput!) {
        ugcArticlePublishSolution(data: $data) {
            article {
                uuid
                slug
                title
            }
        }
    }
    """

    # Extract first sentence of content as summary
    summary = content.split("\n")[0][:200] if content else title

    variables = {
        "data": {
            "questionSlug": slug,
            "title": title,
            "content": content,
            "summary": summary,
            "thumbnail": "",
            "tags": [],
        }
    }

    payload = json.dumps({
        "query": query,
        "variables": variables,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://leetcode.com/graphql/",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Cookie": f"LEETCODE_SESSION={session}; csrftoken={csrf}",
            "x-csrftoken": csrf,
            "Referer": f"https://leetcode.com/problems/{slug}/solutions/",
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://leetcode.com",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if "errors" in data:
            print(f"LeetCode API errors: {json.dumps(data['errors'], indent=2)}", file=sys.stderr)
            sys.exit(1)

        article = data.get("data", {}).get("ugcArticlePublishSolution", {}).get("article", {})
        if article:
            article_slug = article.get("slug", "")
            print(f"Posted: https://leetcode.com/problems/{slug}/solutions/{article_slug}/")
        else:
            print("Post submitted (no article URL returned).")
            print(f"Response: {json.dumps(data, indent=2)}")

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} error: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 4:
        print("Usage: post-to-leetcode.py <slug> <title> <content>", file=sys.stderr)
        sys.exit(1)

    slug = sys.argv[1]
    title = sys.argv[2]
    content = sys.argv[3]
    post_solution(slug, title, content)


if __name__ == "__main__":
    main()
