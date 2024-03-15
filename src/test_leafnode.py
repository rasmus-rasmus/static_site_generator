import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf_node = LeafNode(tag="a", value="Google", props={"href": "http://google.com"})
        self.assertEqual(leaf_node.to_html(), '<a href="http://google.com">Google</a>')
        
    def test_to_html_no_props(self):
        leaf_node = LeafNode(tag="p", value="paragraph")
        self.assertEqual(leaf_node.to_html(), '<p>paragraph</p>')
        
    def test_to_html_no_value(self):
        leaf_node = LeafNode(tag="p", value=None)
        self.assertRaises(ValueError, leaf_node.to_html)
        
    def test_to_html_no_tag(self):
        leaf_node = LeafNode(value="plaintext")
        self.assertEqual(leaf_node.to_html(), "plaintext")