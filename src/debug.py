from textnode import *
from url_extractor import *
from md_to_html import markdown_to_html_node

def main():
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)

    return node.to_html()

print(main())