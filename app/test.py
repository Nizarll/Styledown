from tree_sitter import Language, Parser

# Compile the Tree-sitter Python grammar
Language.build_library(
    'build/my-languages.so',
    [
        'tree-sitter-python'
    ]
)
PYTHON_LANGUAGE = Language('build/my-languages.so', 'python')

# Sample Python code to highlight
code = """
# A simple Python function
def greet(name):
    print(f"Hello, {name}")
greet("World")
"""

# Map syntax types to CSS classes
TYPE_TO_CLASS = {
    "function_definition": "function",
    "string": "string",
    "comment": "comment",
    "keyword": "keyword",
    "identifier": "identifier",
    # Add more as needed
}

# Initialize Tree-sitter parser
parser = Parser()
parser.set_language(PYTHON_LANGUAGE)
tree = parser.parse(bytes(code, "utf8"))

# Walk the Tree-sitter syntax tree
def walk_tree(node, code):
    result = ""
    if node.child_count == 0:
        # Leaf node, get the text with styling
        text = code[node.start_byte : node.end_byte]
        css_class = TYPE_TO_CLASS.get(node.type)
        if css_class:
            return f'<span class="{css_class}">{text}</span>'
        return text

    # Internal node, recurse on children
    for child in node.children:
        result += walk_tree(child, code)
    return result

# Generate highlighted HTML
highlighted_html = walk_tree(tree.root_node, code)

# Create HTML template
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tree-sitter Syntax Highlighting</title>
  <style>
    body {{
      font-family: monospace;
      background-color: #2e3440;
      color: #d8dee9;
      padding: 20px;
    }}
    .token {{
      font-weight: normal;
    }}
    .keyword {{
      color: #81a1c1;
      font-weight: bold;
    }}
    .string {{
      color: #a3be8c;
    }}
    .function {{
      color: #88c0d0;
    }}
    .comment {{
      color: #616e88;
      font-style: italic;
    }}
  </style>
</head>
<body>
  <div id="code-container" style="white-space: pre-wrap;">{highlighted_html}</div>
</body>
</html>
"""

# Write the HTML to a file
with open("highlighted_code.html", "w") as f:
    f.write(html_template)

print("HTML file generated: highlighted_code.html")

