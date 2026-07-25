import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
        #basic tests
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_text_type(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a text node", "With extra fries", "https://www.boot.dev")

        #text_to_html
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
    
    def test_image(self):
        node = TextNode("This is a not a pipe", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is a not a pipe"})

    def test_no_text(self):
        node = TextNode(None, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

        #split_nodes_delimiter
    def test_direct_bold_split(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_node, [TextNode("This is a bold node", TextType.BOLD)])

    def test_bold_split(self):
        node = TextNode("This is a node containing **bold text** !", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(split_node), 3)
        self.assertEqual(split_node[0], TextNode("This is a node containing ", TextType.TEXT))
        self.assertEqual(split_node[1], TextNode("bold text", TextType.BOLD))
        self.assertEqual(split_node[2], TextNode(" !", TextType.TEXT))
    
    def test_two_bold_split(self):
        node = TextNode("This is a node containing **bold text** ! In fact it does **twice** !", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(split_node), 5)
        self.assertEqual(split_node[0], TextNode("This is a node containing ", TextType.TEXT))
        self.assertEqual(split_node[1], TextNode("bold text", TextType.BOLD))
        self.assertEqual(split_node[2], TextNode(" ! In fact it does ", TextType.TEXT))
        self.assertEqual(split_node[3], TextNode("twice", TextType.BOLD))
        self.assertEqual(split_node[4], TextNode(" !", TextType.TEXT))
    
    def test_italic_start_split(self):
        node = TextNode("_Italic text_ initiates this text !", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(split_node), 2)
        self.assertEqual(split_node[0], TextNode("Italic text", TextType.ITALIC))
        self.assertEqual(split_node[1], TextNode(" initiates this text !", TextType.TEXT))

    def test_code_end_split(self):
        node = TextNode("This text ends with `code !`", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(split_node), 2)
        self.assertEqual(split_node[0], TextNode("This text ends with ", TextType.TEXT))
        self.assertEqual(split_node[1], TextNode("code !", TextType.CODE))

    def test_no_text_split(self):
        node = TextNode("", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(split_node, [])
    
    def test_no_delimiter_split(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a bold node", TextType.BOLD)
            split_node = split_nodes_delimiter([node], "", TextType.BOLD)

    def test_no_type_split(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a bold node", TextType.BOLD)
            split_node = split_nodes_delimiter([node], "**", None)
    
    def test_uneven_delimiters_split(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a error **node", TextType.TEXT)
            split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_multiple_nodes_split(self):
        node1 = TextNode("This is a node containing **bold text** !", TextType.TEXT)
        node2 = TextNode("This text ends with `code !`", TextType.TEXT)
        split_node = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(len(split_node), 4)
        self.assertEqual(split_node[0], TextNode("This is a node containing ", TextType.TEXT))
        self.assertEqual(split_node[1], TextNode("bold text", TextType.BOLD))
        self.assertEqual(split_node[2], TextNode(" !", TextType.TEXT))
        self.assertEqual(split_node[3], TextNode("This text ends with `code !`", TextType.TEXT))
        
    def test_plain_text(self):
        node = TextNode("This is plain text", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_node[0], node)

        #Image Split
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        #Link Split
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
        #Text_to_textnode
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
    ])

    def test_empty_text_to_textnodes(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [])
    
    def test_multiple_duplicates_text_to_textnodes(self):
        text = "This is **bold** text with _italic_ and also **more bold** and _more italic_ !"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and also ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more italic", TextType.ITALIC),
            TextNode(" !", TextType.TEXT)
        ])

    def test_uneven_text_to_textnodes(self):
        with self.assertRaises(Exception):
            text = "This is a **bold** attempt at _provoking a bug"
            nodes = text_to_textnodes(text)

class TestBlocks(unittest.TestCase):
        #markdown_to_blocks
    def test_markdown_to_block_simple(self):
        markdown = """\n# Heading\n\nA simple paragraph\nwith multiple lines\n\n- a last list\n- a last list again"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [
            "# Heading",
            "A simple paragraph\nwith multiple lines",
            "- a last list\n- a last list again"
        ])

    def test_markdown_to_block_with_trailing_whitespaces(self):
        markdown = """\n# Heading\n\nA simple paragraph   \n      with multiple lines \n\n- a last list   \n  - a last list again """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [
            "# Heading",
            "A simple paragraph\nwith multiple lines",
            "- a last list\n- a last list again"
        ])

    def test_markdown_to_block_double_newlines(self):
        markdown = """\n# Heading\n\n\nA simple paragraph\nwith multiple lines\n\n- a last list\n- a last list again\n"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [
            "# Heading",
            "A simple paragraph\nwith multiple lines",
            "- a last list\n- a last list again"
        ])

    def test_markdown_to_block_no_text(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [])

    def test_markdown_to_block_list(self):
        with self.assertRaises(ValueError):
            markdown = ["line 1", "line 32"]
            block = markdown_to_blocks(markdown)
    
        ###Block_to_Blocktype###
    def test_block_to_block_type_para(self):
        markdown = "This is txt\nAnd mor t xt"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        markdown = "### This is header 3\n#### And header 4"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_fake_heading(self):
        markdown = "### This is header 3\n####And a surprise not_header"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.HEADING)    

    def test_block_to_block_type_fake_heading_b(self):
        markdown = "### This is header 3\n #### And a surprise not_header"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.HEADING)  
    
    def test_block_to_block_type_quote_notheading(self):
        markdown = ">### if not header, why header shape ?\n> uhhh ???"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.QUOTE)  

    def test_block_to_block_type_code(self):
        markdown = "```\nThis is code\n```"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        markdown = "> I like pigs. Dogs look up to us. Cats look down on us. Pigs treat us as equals.\n>\n>— Sir Winston Churchill "
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_u_list(self):
        markdown = "- truc\n- machin\n- chose"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_u_list(self):
        markdown = "1. truc\n2. machin\n3. chose"
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_empty(self):
        markdown = ""
        block_type = block_to_block_type(markdown)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    

if __name__ == "__main__":
    unittest.main()