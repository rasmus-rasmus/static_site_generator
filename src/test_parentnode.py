import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_one_child(self):
        child_node = LeafNode(tag="b", value="bold face")
        parent_node = ParentNode(tag="p", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<p><b>bold face</b></p>")
        
    def test_to_html_two_children(self):
        child_node = LeafNode(tag="b", value="bold face")
        child_node2 = LeafNode(tag="a", value="Google", props={"href": "http://Google.com"})
        parent_node = ParentNode(tag="p", children=[child_node, child_node2])
        self.assertEqual(parent_node.to_html(), '<p><b>bold face</b><a href="http://Google.com">Google</a></p>')
        
    def test_to_html_nested(self):
        leaf_node = LeafNode(tag="b", value="bold face")
        intermediate_node = ParentNode(tag="p", children=[leaf_node])
        parent_node = ParentNode(tag="div", children=[intermediate_node])
        self.assertEqual(parent_node.to_html(), '<div><p><b>bold face</b></p></div>')
        
    def test_to_html_two_nested(self):
        leaf_node1 = LeafNode(tag="b", value="bold face")
        leaf_node2 = LeafNode(value="just face")
        leaf_node3 = LeafNode(tag="i", value="italic")
        intermediate_node1 = ParentNode(tag="p", children=[leaf_node1, leaf_node2])
        intermediate_node2 = ParentNode(tag="span", children=[leaf_node3])
        parent_node = ParentNode(tag="div", children=[intermediate_node1, intermediate_node2])
        self.assertEqual(parent_node.to_html(), '<div><p><b>bold face</b>just face</p><span><i>italic</i></span></div>')
        
    def test_to_html_no_tag(self):
        leaf_node1 = LeafNode(tag="b", value="bold face")
        parent_node = ParentNode(tag = None, children=[leaf_node1])
        self.assertRaises(ValueError, parent_node.to_html)
        
    def test_to_html_no_children(self):
        parent_node = ParentNode(tag="html", children=None)
        self.assertRaises(ValueError, parent_node.to_html)