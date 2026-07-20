from textnode import TextNode, TextType

def main():
    new = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(new)

main()