from os import path, makedirs


from markdown_to_html import markdown_to_html_node
from utils import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path) as src_file:
        markdown = src_file.read()
    with open(template_path) as tmpl_file:
        template = tmpl_file.read()
        
    html_doc = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_doc)
    
    dir = path.dirname(dest_path)
    if not path.exists(dir):
        makedirs(dir)
        
    with open(dest_path, "w") as dst_file:
        dst_file.write(template)
        