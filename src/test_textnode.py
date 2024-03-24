import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test", "bold", "http://example.com")
        self.assertEqual(text_node_1, text_node_2)
        
    def test_eq_none(self):
        text_node_1 = TextNode("Test", "bold")
        text_node_2 = TextNode("Test", "bold")
        self.assertEqual(text_node_1, text_node_2)
        
    def test_ne(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test", "bold", "http://example.org")
        self.assertNotEqual(text_node_1, text_node_2)
        
    def test_ne_text(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test2", "bold", "http://example.com")
        self.assertNotEqual(text_node_1, text_node_2)
        
    def test_ne_text_type(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test", "italic", "http://example.com")
        self.assertNotEqual(text_node_1, text_node_2)
        
    def test_ne_none(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test", "bold")
        self.assertNotEqual(text_node_1, text_node_2)
        
        
class TestTextNodeToHTML(unittest.TestCase):       
    def test_text_node_to_html(self):
        text_node = TextNode(text="test", text_type=text_type_text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, text_node.text)
        
    def test_text_node_to_html_bold(self):
        text_node = TextNode(text="test", text_type=text_type_bold)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, text_node.text)
        
    def test_text_node_to_html_italic(self):
        text_node = TextNode(text="test", text_type=text_type_italic)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, text_node.text)
        
    def test_text_node_to_html_code(self):
        text_node = TextNode(text="test", text_type=text_type_code)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, text_node.text)
        
    def test_text_node_to_html_link(self):
        text_node = TextNode(text="test", text_type=text_type_link, url="http://ur.l")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, text_node.text)
        self.assertDictEqual(html_node.props, {"href": text_node.url})
        
    def test_text_node_to_html_image(self):
        text_node = TextNode(text="test", text_type=text_type_image, url="http://ur.l")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertDictEqual(html_node.props, {"src": text_node.url, "alt": text_node.text})
        
    def test_text_node_to_html_unknown_type(self):
        text_node = TextNode(text="test", text_type="unknown")
        self.assertRaises(ValueError, text_node_to_html_node, text_node)
        
        

        
if __name__ == "__main__":
    unittest.main()