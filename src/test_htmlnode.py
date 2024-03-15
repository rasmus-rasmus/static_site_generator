import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        html_node = HTMLNode("a", "Google", props={"href": "http://www.google.com"})
        html_node2 = HTMLNode("a", "Amazon", props={"href": "http://www.amazon.com"})
        html_parent = HTMLNode("div", children=[html_node, html_node2])
        self.assertRaises(NotImplementedError, html_parent.to_html)
        
    def test_props_to_html(self):
        html_node = HTMLNode("a", "Google", props={"href": "http://www.google.com"})
        self.assertEqual(html_node.props_to_html(), ' href="http://www.google.com"')
        
    def test_props_to_html_none(self):
        html_node = HTMLNode("div", "This is a div tag")
        self.assertEqual(html_node.props_to_html(), "")
    