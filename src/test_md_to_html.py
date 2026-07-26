import unittest
from textnode import BlockType
from md_to_html import *

class TestMD_to_HTML(unittest.TestCase):
        ###block_to_block_node###
    def test_block_to_block_node_paragraph(self):
        markdown = "This is txt\nAnd more text"
        node = block_to_block_node(markdown, BlockType.PARAGRAPH)
        self.assertEqual(node, HTMLNode("p", "This is txt\nAnd more text"))

    def test_block_to_block_node_headings(self):
        hd1 = "# This is header 1"
        hd2 = "## This is header 2"
        hd3 = "### This is header 3"
        hd4 = "#### This is header 4"
        hd5 = "##### This is header 5"
        hd6 = "###### This is header 6"
        nodes = []
        nodes.append(block_to_block_node(hd1, BlockType.HEADING))
        nodes.append(block_to_block_node(hd2, BlockType.HEADING))
        nodes.append(block_to_block_node(hd3, BlockType.HEADING))
        nodes.append(block_to_block_node(hd4, BlockType.HEADING))
        nodes.append(block_to_block_node(hd5, BlockType.HEADING))
        nodes.append(block_to_block_node(hd6, BlockType.HEADING))
        for i in range(1,7):
            self.assertEqual(nodes[i-1].tag, f"h{i}")
    
    def test_block_to_block_node_UL(self):
        markdown = "- truc\n- machin\n- chose"
        node = block_to_block_node(markdown, BlockType.UNORDERED_LIST)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[1].value, "- machin")

    def test_block_to_block_node_OL(self):
        markdown = "1. truc\n2. machin\n3. chose"
        node = block_to_block_node(markdown, BlockType.ORDERED_LIST)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[1].value, "2. machin")
        
    def test_block_to_block_node_empty(self):
        with self.assertRaises(ValueError):
            markdown = ""
            node = block_to_block_node(markdown, None)