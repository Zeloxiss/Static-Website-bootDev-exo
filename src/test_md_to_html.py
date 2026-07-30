import unittest
from textnode import BlockType
from md_to_html import *

class TestMD_to_HTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_lists(self):
        md = """
- Lorem ipsum: 
- dolor sit amet, 
- **consectetur**
- adipiscing 
- _elit._

1. porttitor 
2. sem 
3. et
4. suscipit.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>Lorem ipsum:</li><li>dolor sit amet,</li><li><b>consectetur</b></li><li>adipiscing</li><li><i>elit.</i></li></ul><ol><li>porttitor</li><li>sem</li><li>et</li><li>suscipit.</li></ol></div>",
    )

    def test_empty(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div></div>",
    )

    def test_headers(self):
        md = """
# hd1

## hd2

#### hd4

###### hd6

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h1>hd1</h1><h2>hd2</h2><h4>hd4</h4><h6>hd6</h6></div>",
    )

    def test_quotes(self):
        md = """
> This is **bolded** quote
> text in a p
> tag here

> This is another quote with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>This is <b>bolded</b> quote\ntext in a p\ntag here</blockquote><blockquote>This is another quote with <i>italic</i> text and <code>code</code> here</blockquote></div>",
    )

    def test_fake_markers_in_a_quote(self):
        md = """
> ## This is not an **h2**
>
> - _Hitchhiker No-tal-ist_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>## This is not an <b>h2</b>\n\n- <i>Hitchhiker No-tal-ist</i></blockquote></div>",
    )

        ###Extract title###
    def test_extract_title_oneline(self):
        md = "#   header 1 "
        title = extract_title(md)
        self.assertEqual(title, "header 1")

    def test_extract_title_lines(self):
        md = """
## hd2

# hd1 

#### hd4

###### hd6

"""
        title = extract_title(md)
        self.assertEqual(title, "hd1")
    
    def test_extract_title_empty(self):
        with self.assertRaises(Exception):
            md = ""
            title = extract_title(md)