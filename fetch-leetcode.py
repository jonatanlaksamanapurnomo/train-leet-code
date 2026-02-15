#!/usr/bin/env python3
"""Fetch LeetCode problem data and generate Main.java with test cases."""

import json
import re
import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser


def fetch_problem(slug):
    """Fetch problem data from LeetCode GraphQL API."""
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            content
            codeSnippets {
                lang
                code
            }
            exampleTestcases
        }
    }
    """
    payload = json.dumps({
        "query": query,
        "variables": {"titleSlug": slug}
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/problems/{slug}/",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["data"]["question"]


class OutputExtractor(HTMLParser):
    """Extract expected outputs from LeetCode HTML content."""

    def __init__(self):
        super().__init__()
        self.outputs = []
        self._capture = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        if tag == "strong":
            self._capture_check = True
            self._buf = ""

    def handle_data(self, data):
        if hasattr(self, "_capture_check") and self._capture_check:
            self._buf += data
            return
        if self._capture:
            self._capture = False
            text = data.strip()
            # Sometimes output is on same line as "Output:"
            if text:
                self.outputs.append(text)

    def handle_endtag(self, tag):
        if tag == "strong" and hasattr(self, "_capture_check") and self._capture_check:
            self._capture_check = False
            if "Output" in self._buf:
                self._capture = True


def extract_outputs(html):
    """Extract expected outputs from problem HTML."""
    # Primary: regex-based extraction (more reliable)
    outputs = []
    pattern = r'<strong>Output:?\s*</strong>\s*(?:</?span[^>]*>\s*)*([^\n<]+)'
    for m in re.finditer(pattern, html):
        val = m.group(1).strip()
        if val:
            outputs.append(val)
    if outputs:
        return outputs
    # Fallback: HTML parser
    parser = OutputExtractor()
    parser.feed(html)
    return parser.outputs


def parse_signature(java_code):
    """Parse Java method signature from code snippet.
    Returns (return_type, method_name, [(param_type, param_name), ...])
    """
    # Match: public <return_type> <method_name>(<params>) {
    m = re.search(
        r'public\s+([\w\[\]<>, ]+?)\s+(\w+)\s*\(([^)]*)\)',
        java_code,
    )
    if not m:
        return None, None, []
    ret_type = m.group(1).strip()
    method_name = m.group(2).strip()
    params_str = m.group(3).strip()
    params = []
    if params_str:
        for p in params_str.split(","):
            p = p.strip()
            parts = p.rsplit(None, 1)
            if len(parts) == 2:
                params.append((parts[0], parts[1]))
    return ret_type, method_name, params


def convert_value(value, java_type):
    """Convert a LeetCode test value to Java syntax based on type."""
    value = value.strip()
    java_type = java_type.strip()

    if java_type == "int" or java_type == "long":
        return value
    if java_type == "double" or java_type == "float":
        return value
    if java_type == "boolean":
        return value
    if java_type == "char":
        # LeetCode gives "a", we need 'a'
        stripped = value.strip('"')
        return f"'{stripped}'"
    if java_type == "String":
        if not value.startswith('"'):
            return f'"{value}"'
        return value

    if java_type == "int[]":
        return f"new int[]{{{_array_inner(value)}}}"
    if java_type == "long[]":
        return f"new long[]{{{_array_inner(value)}}}"
    if java_type == "double[]":
        return f"new double[]{{{_array_inner(value)}}}"
    if java_type == "char[]":
        inner = value.strip("[]")
        items = [x.strip().strip('"') for x in inner.split(",") if x.strip()]
        return "new char[]{" + ", ".join(f"'{c}'" for c in items) + "}"
    if java_type == "String[]":
        inner = value.strip("[]")
        items = [x.strip() for x in _split_top_level(inner) if x.strip()]
        converted = []
        for item in items:
            if not item.startswith('"'):
                item = f'"{item}"'
            converted.append(item)
        return "new String[]{" + ", ".join(converted) + "}"
    if java_type == "boolean[]":
        return f"new boolean[]{{{_array_inner(value)}}}"

    if java_type == "int[][]":
        return _convert_2d_array(value, "int")
    if java_type == "char[][]":
        return _convert_2d_char_array(value)
    if java_type == "String[][]":
        return _convert_2d_string_array(value)

    if java_type == "List<Integer>":
        return f"List.of({_array_inner(value)})"
    if java_type == "List<String>":
        inner = value.strip("[]")
        items = [x.strip() for x in _split_top_level(inner) if x.strip()]
        converted = []
        for item in items:
            if not item.startswith('"'):
                item = f'"{item}"'
            converted.append(item)
        return "List.of(" + ", ".join(converted) + ")"
    if java_type == "List<List<Integer>>":
        return _convert_list_of_list(value, "Integer")
    if java_type == "List<List<String>>":
        return _convert_list_of_list(value, "String")

    if java_type in ("TreeNode", "ListNode"):
        return f"null /* TODO: build from {value} */"

    # Fallback
    return value


def _array_inner(value):
    """Extract inner content of [...] and add spaces after commas."""
    inner = value.strip("[]")
    items = [x.strip() for x in inner.split(",") if x.strip()]
    return ", ".join(items)


def _split_top_level(s):
    """Split string by commas, respecting brackets and quotes."""
    items = []
    depth = 0
    in_str = False
    current = ""
    for c in s:
        if c == '"' and (not current or current[-1] != '\\'):
            in_str = not in_str
            current += c
        elif in_str:
            current += c
        elif c in ('[', '{', '('):
            depth += 1
            current += c
        elif c in (']', '}', ')'):
            depth -= 1
            current += c
        elif c == ',' and depth == 0:
            items.append(current)
            current = ""
        else:
            current += c
    if current:
        items.append(current)
    return items


def _convert_2d_array(value, base_type):
    """Convert [[1,2],[3,4]] to new int[][]{{1, 2}, {3, 4}}."""
    value = value.strip()
    # Remove outer brackets
    inner = value[1:-1].strip()
    rows = _split_top_level(inner)
    converted_rows = []
    for row in rows:
        row = row.strip()
        row_inner = row.strip("[]")
        items = [x.strip() for x in row_inner.split(",") if x.strip()]
        converted_rows.append("{" + ", ".join(items) + "}")
    return f"new {base_type}[][]{{{', '.join(converted_rows)}}}"


def _convert_2d_char_array(value):
    """Convert [["a","b"],["c"]] to new char[][]{{'a','b'},{'c'}}."""
    inner = value[1:-1].strip()
    rows = _split_top_level(inner)
    converted_rows = []
    for row in rows:
        row = row.strip().strip("[]")
        items = [x.strip().strip('"') for x in row.split(",") if x.strip()]
        converted_rows.append("{" + ", ".join(f"'{c}'" for c in items) + "}")
    return f"new char[][]{{{', '.join(converted_rows)}}}"


def _convert_2d_string_array(value):
    """Convert [["a","b"],["c"]] to new String[][]{{"a","b"},{"c"}}."""
    inner = value[1:-1].strip()
    rows = _split_top_level(inner)
    converted_rows = []
    for row in rows:
        row = row.strip().strip("[]")
        items = [x.strip() for x in _split_top_level(row) if x.strip()]
        converted = []
        for item in items:
            if not item.startswith('"'):
                item = f'"{item}"'
            converted.append(item)
        converted_rows.append("{" + ", ".join(converted) + "}")
    return f"new String[][]{{{', '.join(converted_rows)}}}"


def _convert_list_of_list(value, element_type):
    """Convert [[1,2],[3]] to List.of(List.of(1,2),List.of(3))."""
    inner = value[1:-1].strip()
    rows = _split_top_level(inner)
    converted = []
    for row in rows:
        row = row.strip().strip("[]")
        items = [x.strip() for x in row.split(",") if x.strip()]
        converted.append(f"List.of({', '.join(items)})")
    return f"List.of({', '.join(converted)})"


def needs_arrays_import(ret_type, params):
    """Check if Arrays import is needed."""
    array_types = [t for t, _ in params if "[]" in t]
    return "[]" in ret_type or array_types


def needs_list_import(ret_type, params):
    """Check if List import is needed."""
    all_types = [ret_type] + [t for t, _ in params]
    return any("List<" in t for t in all_types)


def build_print_wrapper(ret_type, call_expr):
    """Build the System.out.println statement with appropriate wrapper."""
    if "[][]" in ret_type:
        return f"System.out.println(Arrays.deepToString({call_expr}));"
    if "[]" in ret_type:
        return f"System.out.println(Arrays.toString({call_expr}));"
    return f"System.out.println({call_expr});"


def generate_java(slug, question):
    """Generate complete Main.java content."""
    qid = question["questionId"]
    title = question["title"]
    html = question["content"]
    example_inputs = question["exampleTestcases"]
    code_snippets = question["codeSnippets"]

    # Find Java snippet
    java_code = None
    for snippet in code_snippets:
        if snippet["lang"] == "Java":
            java_code = snippet["code"]
            break
    if not java_code:
        raise ValueError("No Java code snippet found")

    ret_type, method_name, params = parse_signature(java_code)
    if not method_name:
        raise ValueError("Could not parse method signature")

    # Parse test inputs
    raw_inputs = [line for line in example_inputs.strip().split("\n") if line.strip()]
    num_params = len(params)
    if num_params == 0:
        raise ValueError("No parameters found in method signature")

    # Group inputs into test cases
    test_cases = []
    for i in range(0, len(raw_inputs), num_params):
        if i + num_params <= len(raw_inputs):
            test_cases.append(raw_inputs[i:i + num_params])

    # Extract expected outputs
    outputs = extract_outputs(html)

    # Build imports
    imports = []
    use_arrays = needs_arrays_import(ret_type, params)
    use_list = needs_list_import(ret_type, params)
    if use_arrays:
        imports.append("import java.util.Arrays;")
    if use_list:
        imports.append("import java.util.List;")

    # Build output lines
    lines = []
    lines.append(f"// {qid}. {title}")
    lines.append(f"// https://leetcode.com/problems/{slug}/")
    lines.append("")
    for imp in imports:
        lines.append(imp)
    if imports:
        lines.append("")
    # Solution class from LeetCode
    lines.append(java_code.rstrip())
    lines.append("")
    lines.append("public class Main {")
    lines.append("    public static void main(String[] args) {")
    lines.append("        Solution solution = new Solution();")

    is_void = ret_type == "void"

    for idx, tc in enumerate(test_cases):
        lines.append("")
        # Build comment
        param_strs = []
        for j, (ptype, pname) in enumerate(params):
            param_strs.append(f"{pname} = {tc[j]}")
        comment_parts = ", ".join(param_strs)
        if idx < len(outputs):
            comment = f"// Example {idx + 1}: {comment_parts} -> Output: {outputs[idx]}"
        else:
            comment = f"// Example {idx + 1}: {comment_parts}"
        lines.append(f"        {comment}")

        # Build method call arguments
        args = []
        for j, (ptype, pname) in enumerate(params):
            args.append(convert_value(tc[j], ptype))
        args_str = ", ".join(args)

        if is_void:
            # For void methods: declare variable for first array param, call, then print
            # Find first array/list param to print after mutation
            print_param = None
            decl_lines = []
            call_args = []
            for j, (ptype, pname) in enumerate(params):
                converted = convert_value(tc[j], ptype)
                if "[]" in ptype and print_param is None:
                    # Declare as local variable
                    decl_lines.append(
                        f"        {ptype} {pname}{idx + 1} = {converted};"
                    )
                    call_args.append(f"{pname}{idx + 1}")
                    print_param = (ptype, f"{pname}{idx + 1}")
                else:
                    call_args.append(converted)
            for dl in decl_lines:
                lines.append(dl)
            call_args_str = ", ".join(call_args)
            lines.append(
                f"        solution.{method_name}({call_args_str});"
            )
            if print_param:
                ptype, var_name = print_param
                lines.append(
                    f"        {build_print_wrapper(ptype, var_name)}"
                )
        else:
            call_expr = f"solution.{method_name}({args_str})"
            lines.append(f"        {build_print_wrapper(ret_type, call_expr)}")

    lines.append("    }")
    lines.append("}")
    lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch-leetcode.py <problem-slug>", file=sys.stderr)
        sys.exit(1)

    slug = sys.argv[1]
    try:
        question = fetch_problem(slug)
        if not question:
            print(f"Error: Problem '{slug}' not found", file=sys.stderr)
            sys.exit(1)
        output = generate_java(slug, question)
        print(output, end="")
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, KeyError, TypeError) as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
