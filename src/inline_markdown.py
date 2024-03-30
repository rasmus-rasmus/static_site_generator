from textnode import *


def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes += [old_node]
            continue
        new_node_texts = old_node.text.split(delimeter)
        if len(new_node_texts) % 2 != 1:
            raise ValueError("No matching closing delimeter")
        for index in range(len(new_node_texts)):
            text = new_node_texts[index]
            if len(text) == 0:
                if index == 0 or index == len(new_node_texts)-1:
                    continue
                raise RuntimeError("Empty word in string")
            if index % 2 == 0:
                new_nodes += [TextNode(text=text, text_type=old_node.text_type, url=old_node.url)]
            else:
                new_nodes += [TextNode(text=text, text_type=text_type)]
    
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern=pattern, string=text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern=pattern, string=text)

def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes += [old_node]
            continue
        remaining_text = old_node.text
        images = extract_markdown_images(old_node.text)
        for image in images:
            [prefix, remaining_text] = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(prefix):
                new_nodes += [TextNode(prefix, text_type_text)]
            new_nodes += [TextNode(image[0], text_type_image, image[1])]
        if len(remaining_text):
            new_nodes += [TextNode(remaining_text, text_type_text)]
    
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes += [old_node]
            continue
        remaining_text = old_node.text
        links = extract_markdown_links(old_node.text)
        for link in links:
            [prefix, remaining_text] = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(prefix):
                new_nodes += [TextNode(prefix, text_type_text)]
            new_nodes += [TextNode(link[0], text_type_link, link[1])]
        if len(remaining_text):
            new_nodes += [TextNode(remaining_text, text_type_text)]
    
    return new_nodes
        

def text_to_text_nodes(text):
    text_node = [TextNode(text, text_type_text)]
    images_extracted = split_nodes_images(text_node)
    links_extracted = split_nodes_links(images_extracted)
    bold_extracted = split_nodes_delimeter(links_extracted, "**", text_type_bold)
    italic_extracted = split_nodes_delimeter(bold_extracted, "*", text_type_italic)
    italic_extracted = split_nodes_delimeter(italic_extracted, "_", text_type_italic)
    code_extracted = split_nodes_delimeter(italic_extracted, "`", text_type_code)
    return code_extracted
 