from textnode import *
from url_extractor import *
from md_to_html import markdown_to_html_node
import re

def main():
    md = """
# hd1

## hd2

#### hd4

###### hd6

"""
    node = markdown_to_html_node(md)

    return node.to_html()

print(main())