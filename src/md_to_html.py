from htmlnode import *
from textnode import *
import re

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    block_nodes = [] 
    for block in blocks:
        block_node = block_to_block_node(block, block_to_block_type(block))
        block_nodes.append(block_node)
    return ParentNode("div", block_nodes)

        
def block_to_block_node(block: str, block_type: BlockType) -> ParentNode(str, list):
    if not isinstance(block_type, BlockType):
        raise ValueError("block_type is not a BlockType")

    match block_type:
        case BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            children_nodes = text_to_children(block)
            block_node = ParentNode("p", children_nodes)

        case BlockType.HEADING:
            for i in range(1,7):
                if re.match(f"^([#]{{{i}}})[ ]", block) != None:
                    children_nodes = text_to_children(block[i+1:])
                    block_node = ParentNode(f"h{i}", children_nodes)
                    return block_node
            raise Exception("Heading passed 6 without finding a match")

        case BlockType.CODE:
            block = block[4:-3]
            node = ParentNode("code", [LeafNode(None, block)])
            block_node = ParentNode("pre", [node])

        case BlockType.QUOTE:
            children_nodes = text_to_children(remove_quote_marker(block))
            block_node = ParentNode("blockquote", children_nodes)

        case BlockType.UNORDERED_LIST:
            children = []
            lines = block.split("\n")
            for line in lines:
                children_nodes = text_to_children(line[2:])
                line_node = ParentNode("li", children_nodes)
                children.append(line_node)
            block_node = ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            children = []
            lines = block.split("\n")
            for line in lines:
                children_nodes = text_to_children(line[3:])
                line_node = ParentNode("li", children_nodes)
                children.append(line_node)
            block_node = ParentNode("ol", children)
    
    return block_node

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def remove_quote_marker(block: str) -> str:
    lines = block.split("\n")
    trimmed_lines = []
    for line in lines:
        trimmed_lines.append(line[2:])
    return "\n".join(trimmed_lines)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if re.match("^# ", block) != None:
            return block[2:].strip(" ")
    raise Exception("No Header1 was found in markdown text")