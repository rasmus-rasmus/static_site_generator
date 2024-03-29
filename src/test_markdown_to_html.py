import unittest

from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = """## This is a heading
        
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        
        ```This is code```
        """
        html_node = markdown_to_html_node(markdown)
        
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 5)
        