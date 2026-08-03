from textnode import *
from url_extractor import *
from constants import ROOT_DIR, STATIC_DIR, DOCS_DIR, CONTENT_DIR
from md_to_html import markdown_to_html_node, extract_title
from copystatic import copy_directory, clean_dir
from generatepage import generate_pages_recursive
import sys

def get_basepath():
    if len(sys.argv) < 2:
        return "/"
    return sys.argv[1]

def main():
    clean_dir(DOCS_DIR)
    copy_directory(STATIC_DIR, DOCS_DIR)
    basepath = get_basepath()
    generate_pages_recursive(CONTENT_DIR, DOCS_DIR, basepath)


main()