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
            difficulty
            topicTags { name slug }
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


def fetch_daily_slug():
    """Fetch today's daily challenge problem slug from LeetCode."""
    query = """
    query questionOfToday {
        activeDailyCodingChallengeQuestion {
            date
            link
            question {
                titleSlug
            }
        }
    }
    """
    payload = json.dumps({"query": query}).encode("utf-8")

    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["data"]["activeDailyCodingChallengeQuestion"]["question"]["titleSlug"]


def fetch_metadata(slug):
    """Fetch lightweight metadata (difficulty + tags) from LeetCode GraphQL API."""
    query = """
    query questionMeta($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            difficulty
            topicTags { name slug }
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


def build_comparison(ret_type, result_var, expected_var):
    """Build Java comparison expression based on return type."""
    if "[][]" in ret_type:
        return f"Arrays.deepEquals({result_var}, {expected_var})"
    if "[]" in ret_type:
        return f"Arrays.equals({result_var}, {expected_var})"
    if ret_type == "String" or "List<" in ret_type:
        return f"{result_var}.equals({expected_var})"
    if ret_type in ("double", "float"):
        return f"Math.abs({result_var} - {expected_var}) < 1e-5"
    # primitives: int, long, boolean, char
    return f"{result_var} == {expected_var}"


def build_display(ret_type, var):
    """Build Java expression to display a value as string."""
    if "[][]" in ret_type:
        return f"Arrays.deepToString({var})"
    if "[]" in ret_type:
        return f"Arrays.toString({var})"
    return var


def _emit_judge(lines, idx, ret_type, result_var, expected_val):
    """Emit PASS/FAIL judge block for a test case."""
    n = idx + 1
    lines.append(f"        {ret_type} expected{n} = {expected_val};")
    comp = build_comparison(ret_type, result_var, f"expected{n}")
    disp_r = build_display(ret_type, result_var)
    disp_e = build_display(ret_type, f"expected{n}")
    lines.append(f"        if ({comp}) {{")
    lines.append(f'            System.out.println("Test {n}: PASS");')
    lines.append(f"            passed++;")
    lines.append(f"        }} else {{")
    lines.append(
        f'            System.out.println("Test {n}: FAIL'
        f' (expected: " + {disp_e} + ", got: " + {disp_r} + ")");'
    )
    lines.append(f"        }}")


def _emit_data_array(lines, arr_type, var_name, values, elem_type):
    """Emit a Java array declaration, using multi-line format for complex types."""
    is_generic = "List<" in elem_type
    if is_generic:
        lines.append(f'        @SuppressWarnings("unchecked")')
        raw_type = re.sub(r'<[^>]+>', '', elem_type)
        prefix = f"new {raw_type}[]"
    else:
        prefix = ""

    inner = ", ".join(values)
    single_line = f"        {arr_type} {var_name} = {prefix}{{{inner}}};"
    use_multiline = len(single_line) > 100 or ("[]" in elem_type and len(values) > 1)

    if use_multiline:
        lines.append(f"        {arr_type} {var_name} = {prefix}{{")
        for i, v in enumerate(values):
            comma = "," if i < len(values) - 1 else ""
            lines.append(f"            {v}{comma}")
        lines.append(f"        }};")
    else:
        lines.append(single_line)


def generate_java(slug, question):
    """Generate Main.java with judge-style PASS/FAIL test output."""
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

    is_void = ret_type == "void"

    # Build output lines
    lines = []
    lines.append(f"// {qid}. {title}")
    lines.append(f"// https://leetcode.com/problems/{slug}/")
    lines.append("")
    for imp in imports:
        lines.append(imp)
    if imports:
        lines.append("")
    lines.append(java_code.rstrip())
    lines.append("")
    lines.append("public class Main {")
    lines.append("    public static void main(String[] args) {")
    lines.append("        Solution solution = new Solution();")
    lines.append("        int passed = 0;")
    lines.append("        int total = 0;")

    all_have_expected = len(outputs) >= len(test_cases) and len(test_cases) > 0

    if all_have_expected:
        # Loop-based test generation
        lines.append("")

        if is_void:
            # Identify the mutated array param
            mutated_idx = None
            for j, (ptype, pname) in enumerate(params):
                if "[]" in ptype:
                    mutated_idx = j
                    break

            # Declare data arrays for each parameter
            for j, (ptype, pname) in enumerate(params):
                values = [convert_value(tc[j], ptype) for tc in test_cases]
                _emit_data_array(lines, ptype + "[]", pname + "Data", values, ptype)

            # Declare expected data array
            if mutated_idx is not None:
                m_type = params[mutated_idx][0]
                exp_values = [convert_value(outputs[idx], m_type) for idx in range(len(test_cases))]
                _emit_data_array(lines, m_type + "[]", "expectedData", exp_values, m_type)

            # For loop
            first_pname = params[0][1]
            lines.append("")
            lines.append(f"        for (int i = 0; i < {first_pname}Data.length; i++) {{")
            lines.append(f"            total++;")
            call_args = [f"{pname}Data[i]" for _, pname in params]
            args_str = ", ".join(call_args)
            lines.append(f"            solution.{method_name}({args_str});")

            if mutated_idx is not None:
                m_type = params[mutated_idx][0]
                m_name = params[mutated_idx][1]
                m_var = f"{m_name}Data[i]"
                comp = build_comparison(m_type, m_var, "expectedData[i]")
                disp_r = build_display(m_type, m_var)
                disp_e = build_display(m_type, "expectedData[i]")
            else:
                comp = "false /* TODO: add comparison */"
                disp_r = '"?"'
                disp_e = '"?"'

            lines.append(f"            if ({comp}) {{")
            lines.append(f'                System.out.println("Test " + (i + 1) + ": PASS");')
            lines.append(f"                passed++;")
            lines.append(f"            }} else {{")
            lines.append(
                f'                System.out.println("Test " + (i + 1) + ": FAIL'
                f' (expected: " + {disp_e} + ", got: " + {disp_r} + ")");'
            )
            lines.append(f"            }}")
            lines.append(f"        }}")

        else:
            # Non-void method
            # Declare data arrays for each parameter
            for j, (ptype, pname) in enumerate(params):
                values = [convert_value(tc[j], ptype) for tc in test_cases]
                _emit_data_array(lines, ptype + "[]", pname + "Data", values, ptype)

            # Declare expected data array
            exp_values = [convert_value(outputs[idx], ret_type) for idx in range(len(test_cases))]
            _emit_data_array(lines, ret_type + "[]", "expectedData", exp_values, ret_type)

            # For loop
            first_pname = params[0][1]
            lines.append("")
            lines.append(f"        for (int i = 0; i < {first_pname}Data.length; i++) {{")
            lines.append(f"            total++;")
            call_args = [f"{pname}Data[i]" for _, pname in params]
            args_str = ", ".join(call_args)
            lines.append(f"            {ret_type} result = solution.{method_name}({args_str});")

            comp = build_comparison(ret_type, "result", "expectedData[i]")
            disp_r = build_display(ret_type, "result")
            disp_e = build_display(ret_type, "expectedData[i]")

            lines.append(f"            if ({comp}) {{")
            lines.append(f'                System.out.println("Test " + (i + 1) + ": PASS");')
            lines.append(f"                passed++;")
            lines.append(f"            }} else {{")
            lines.append(
                f'                System.out.println("Test " + (i + 1) + ": FAIL'
                f' (expected: " + {disp_e} + ", got: " + {disp_r} + ")");'
            )
            lines.append(f"            }}")
            lines.append(f"        }}")

    else:
        # Fallback: per-test-case generation when not all expected outputs are available
        for idx, tc in enumerate(test_cases):
            n = idx + 1
            has_expected = idx < len(outputs)
            lines.append("")

            param_strs = []
            for j, (ptype, pname) in enumerate(params):
                param_strs.append(f"{pname} = {tc[j]}")
            comment_parts = ", ".join(param_strs)
            if has_expected:
                comment = f"// Test {n}: {comment_parts} -> Expected: {outputs[idx]}"
            else:
                comment = f"// Test {n}: {comment_parts}"
            lines.append(f"        {comment}")
            lines.append("        total++;")

            if is_void:
                mutated_param = None
                decl_lines = []
                call_args = []
                for j, (ptype, pname) in enumerate(params):
                    converted = convert_value(tc[j], ptype)
                    if "[]" in ptype and mutated_param is None:
                        decl_lines.append(
                            f"        {ptype} {pname}{n} = {converted};"
                        )
                        call_args.append(f"{pname}{n}")
                        mutated_param = (ptype, f"{pname}{n}")
                    else:
                        call_args.append(converted)
                for dl in decl_lines:
                    lines.append(dl)
                call_args_str = ", ".join(call_args)
                lines.append(
                    f"        solution.{method_name}({call_args_str});"
                )
                if mutated_param and has_expected:
                    ptype, var_name = mutated_param
                    expected_val = convert_value(outputs[idx], ptype)
                    _emit_judge(lines, idx, ptype, var_name, expected_val)
                elif mutated_param:
                    ptype, var_name = mutated_param
                    disp = build_display(ptype, var_name)
                    lines.append(
                        f'        System.out.println("Test {n}: " + {disp});'
                    )
            else:
                call_args = []
                for j, (ptype, pname) in enumerate(params):
                    call_args.append(convert_value(tc[j], ptype))
                args_str = ", ".join(call_args)
                call_expr = f"solution.{method_name}({args_str})"
                lines.append(
                    f"        {ret_type} result{n} = {call_expr};"
                )
                if has_expected:
                    expected_val = convert_value(outputs[idx], ret_type)
                    _emit_judge(lines, idx, ret_type, f"result{n}", expected_val)
                else:
                    disp = build_display(ret_type, f"result{n}")
                    lines.append(
                        f'        System.out.println("Test {n}: " + {disp});'
                    )

    lines.append("")
    lines.append('        System.out.println("\\n" + passed + "/" + total + " tests passed.");')
    lines.append("    }")
    lines.append("}")
    lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch-leetcode.py <problem-slug>", file=sys.stderr)
        print("       fetch-leetcode.py --daily-slug", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--daily-slug":
        try:
            slug = fetch_daily_slug()
            print(slug, end="")
        except Exception as e:
            print(f"Error fetching daily challenge: {e}", file=sys.stderr)
            sys.exit(1)
        return

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
