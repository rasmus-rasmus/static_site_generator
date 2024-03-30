import unittest

from utils import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is the title\n\nThis is just a paragraph"
        title = extract_title(markdown)
        self.assertEqual(title, "This is the title")
        
    def test_extract_title_not_at_top(self):
        markdown = "This is a preamble\n\n# This is the title\n\nAnd this is a paragraph"
        title = extract_title(markdown)
        self.assertEqual(title, "This is the title")
        
    def test_extract_title_no_content(self):
        markdown = "# This is just a title"
        title = extract_title(markdown)
        self.assertEqual(title, "This is just a title")
        
    def test_extract_title_including_newline(self):
        markdown = "# This is a title\nspanning multiple lines\n\nAnd this is a paragraph"
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title spanning multiple lines")
        
    def test_extract_title_containing_subheading(self):
        markdown = "# This is the title\n\nThis is a paragraph\n\n## This is a subheading\n\nAnd another paragraph"
        title = extract_title(markdown)
        self.assertEqual(title, "This is the title")
        
    def test_extract_title_no_title(self):
        markdown = "This document has no title!!"
        self.assertRaises(ValueError, extract_title, markdown)
        
    def test_extract_title_multiple_titles(self):
        markdown = "# Here's a title\n\nHere's a paragraph\n\n# And here's a second title!!"
        self.assertRaises(ValueError, extract_title, markdown)