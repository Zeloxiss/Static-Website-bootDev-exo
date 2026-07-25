from textnode import *
from url_extractor import *

def main():
    block = "```\nThis is code\n```"
    if block[:4] == "```\n":
        print("A")
    if block[-4:] == "\n```":
        print("B")
    #         return True
    # return False
    return "C"



print(main())