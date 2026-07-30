from textnode import *
from url_extractor import *
from constants import ROOT_DIR
from md_to_html import markdown_to_html_node, extract_title
from copystatic import static_to_public, clean_public_dir
from generatepage import generate_pages_recursive

def main():
    clean_public_dir()
    static_to_public()
    generate_pages_recursive(ROOT_DIR + "/content", ROOT_DIR + "/public")

main()