from enum import Enum
from htmlnode import LeafNode
from url_extractor import *
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

        if self.text is None:
            self.text = ""
        if not isinstance(self.text_type, TextType):
            raise ValueError(f'{self.text_type} is not a TextType')
    
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

def text_to_textnodes(text):
    pass
    #???



def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    if not isinstance(delimiter, str) or delimiter == "":
        raise ValueError("Delimiter must be a string")
    if not isinstance(text_type, TextType):
        raise ValueError("text_type must be a TextType")
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            separated_nodes_text = node.text.split(delimiter)
            if len(separated_nodes_text) % 2 == 0:
                raise Exception("Delimiter error: A delimited section is not closed")
            
            reassembled_nodes = []
            for i in range(len(separated_nodes_text)):
                if separated_nodes_text[i] == "":
                    continue
                if i % 2 == 0:
                    reassembled_nodes.append(TextNode(separated_nodes_text[i], TextType.TEXT))
                else:
                    reassembled_nodes.append(TextNode(separated_nodes_text[i], text_type))
            
            new_nodes.extend(reassembled_nodes)
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            raise ValueError("Node TextType is not text")
        
        extracted_images = extract_markdown_images(node.text)
        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue
        else:
            last_node_text = node.text
            separated_nodes_text = []

            for i in range(len(extracted_images)):
                current_image = extracted_images[i]
                temp_split = last_node_text.split(f"![{current_image[0]}]({current_image[1]})", 1)
                separated_nodes_text.append(temp_split[0])
                separated_nodes_text.append(extracted_images[i])
                last_node_text = temp_split[1]
            separated_nodes_text.append(last_node_text)

            if len(separated_nodes_text) % 2 == 0:
                    raise Exception("Unexpected error: even splits happened")

            reassembled_nodes = []
            for i in range(len(separated_nodes_text)):
                if separated_nodes_text[i] == "":
                    continue
                if i % 2 == 0:
                    reassembled_nodes.append(TextNode(separated_nodes_text[i], TextType.TEXT))
                else:
                    reassembled_nodes.append(TextNode(separated_nodes_text[i][0], TextType.IMAGE, separated_nodes_text[i][1]))
                    
            new_nodes.extend(reassembled_nodes)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            raise ValueError("Node TextType is not text")
        
        extracted_links = extract_markdown_links(node.text)
        if len(extracted_links) == 0:
            new_nodes.append(node)
            continue
        else:
            last_node_text = node.text
            separated_nodes_text = []

            for i in range(len(extracted_links)):
                current_link = extracted_links[i]
                temp_split = last_node_text.split(f"[{current_link[0]}]({current_link[1]})", 1)
                separated_nodes_text.append(temp_split[0])
                separated_nodes_text.append(extracted_links[i])
                last_node_text = temp_split[1]
            separated_nodes_text.append(last_node_text)

            if len(separated_nodes_text) % 2 == 0:
                    raise Exception("Unexpected error: even splits happened")

            reassembled_nodes = []
            for i in range(len(separated_nodes_text)):
                if separated_nodes_text[i] == "":
                    continue
                if i % 2 == 0:
                    reassembled_nodes.append(TextNode(separated_nodes_text[i], TextType.TEXT))
                else:
                    reassembled_nodes.append(TextNode(separated_nodes_text[i][0], TextType.LINK, separated_nodes_text[i][1]))
                    
            new_nodes.extend(reassembled_nodes)
    return new_nodes