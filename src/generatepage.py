from constants import DEFAULT_TEMPLATE_PATH
from md_to_html import markdown_to_html_node, extract_title
from htmlnode import HTMLNode
import os

def generate_page(from_path, dest_path, basepath, template_path = DEFAULT_TEMPLATE_PATH):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    md = markdown_file.read()
    template_file = open(template_path)
    template = template_file.read()

    html_node = markdown_to_html_node(md)
    content = html_node.to_html()
    title = extract_title(md)

    filled_template = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    final_template = filled_template.replace('href="/', f'href"{basepath}').replace('src="/', f'src"{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    html_page = open(dest_path, "x")
    html_page.write(final_template)

def generate_pages_recursive(dir_path_content, dest_dir_path, basepath, template_path = DEFAULT_TEMPLATE_PATH):
    content_entries = os.listdir(dir_path_content)
    for entry in content_entries:
        entry_path = os.path.join(dir_path_content, entry)
        entry_dest = os.path.join(dest_dir_path, entry)

        if os.path.isdir(entry_path):
            os.mkdir(entry_dest)
            generate_pages_recursive(entry_path, entry_dest, basepath, template_path)
        if os.path.isfile(entry_path) and entry_path.endswith(".md"):
            html_dest = entry_dest.replace(".md", ".html")
            generate_page(entry_path, html_dest, basepath, template_path)


