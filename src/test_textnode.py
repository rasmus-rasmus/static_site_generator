import unittest

from textnode import TextNode


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
        
if __name__ == "__main__":
    unittest.main()