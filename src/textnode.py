from htmlnode import LeafNode
import re


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type!r}, {self.url!r})"
    
    
def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(value=text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Unknown text type: {text_node.text_type}")


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
        
            