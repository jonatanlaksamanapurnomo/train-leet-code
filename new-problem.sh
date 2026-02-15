#!/bin/bash

# Usage: ./new-problem.sh <leetcode-url>
# Example: ./new-problem.sh https://leetcode.com/problems/two-sum/

if [ -z "$1" ]; then
    echo "Usage: ./new-problem.sh <leetcode-url>"
    echo "Example: ./new-problem.sh https://leetcode.com/problems/two-sum/"
    exit 1
fi

URL="$1"

# Extract problem slug from URL (e.g., "two-sum" from "https://leetcode.com/problems/two-sum/")
SLUG=$(echo "$URL" | sed -E 's|.*/problems/([^/]+)/?.*|\1|')

if [ -z "$SLUG" ]; then
    echo "Error: Could not extract problem name from URL"
    exit 1
fi

FOLDER="$SLUG"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if folder already exists
if [ -d "$FOLDER" ]; then
    echo "Error: Folder '$FOLDER' already exists"
    exit 1
fi

# Create folder structure
mkdir -p "$FOLDER/src"

# Try to fetch from LeetCode and generate Main.java with test cases
GENERATED=$(python3 "$SCRIPT_DIR/fetch-leetcode.py" "$SLUG" 2>/dev/null)

if [ $? -eq 0 ] && [ -n "$GENERATED" ]; then
    echo "$GENERATED" > "$FOLDER/src/Main.java"
    # Extract problem title from first line (e.g., "// 1. Two Sum")
    TITLE=$(head -1 "$FOLDER/src/Main.java" | sed 's|^// ||')
else
    echo "Warning: Could not fetch from LeetCode, using template"
    TITLE="$SLUG"
    cat > "$FOLDER/src/Main.java" << EOF
// $SLUG
// $URL

class Solution {
    // TODO: implement solution
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();

        // TODO: add test cases
    }
}
EOF
fi

echo "Created: $FOLDER/"
echo "  src/Main.java"
echo ""
echo "Problem: $TITLE"
echo "Open: $FOLDER/src/Main.java"
