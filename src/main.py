from textnode import *
from url_extractor import *

def main():
    node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
    
    print("\n\n")
    split_nodes_image([node])
    # print(split_nodes_image([node]))
main()