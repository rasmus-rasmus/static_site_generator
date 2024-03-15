from htmlnode import LeafNode


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