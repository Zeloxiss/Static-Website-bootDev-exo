from htmlnode import *
from textnode import *
import re

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_block_node(block, block_type)
        
        
def block_to_block_node(block, block_type):
    if not isinstance(block_type, BlockType):
        raise ValueError("block_type is not a BlockType")
    match block_type:
        case BlockType.PARAGRAPH:
            return LeafNode("p", block)
        case BlockType.HEADING:
            for i in range(1,7):
                if re.match(f"^([#]{{{i}}})[ ]", block):
                    return LeafNode(f"h{i}", block)
            raise Exception("Heading passed 6 without finding a match")
        case BlockType.CODE:
            node = LeafNode("code", block)
            return ParentNode("pre", [node])
        case BlockType.QUOTE:
            return LeafNode("blockquote", block)
        case BlockType.UNORDERED_LIST:
            children = []
            lines = block.split("\n")
            for line in lines:
                line_node = LeafNode("li", line)
                children.append(line_node)
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            children = []
            lines = block.split("\n")
            for line in lines:
                line_node = LeafNode("li", line)
                children.append(line_node)
            return ParentNode("ol", children)

def text_to_children(text):
    pass
