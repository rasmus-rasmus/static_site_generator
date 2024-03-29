import unittest

from block_markdown import *


class TestMarkdownToBlocks(unittest.TestCase):
    def test_three_blocks(self):
        markdown = """This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        """
        blocks = markdown_to_blocks(markdown)
        
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "This is **bolded** paragraph")
        self.assertEqual(blocks[1], "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line")
        self.assertEqual(blocks[2], "* This is a list\n* with items")
        
    def test_excessive_new_lines(self):
        markdown = """This is a block
        
        
        
        and this is another"""
        blocks = markdown_to_blocks(markdown)
        
        self.assertListEqual(blocks, ["This is a block", "and this is another"])
        
        
class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        heading_1 = "# This is a heading"
        heading_2 = "### And this is too"
        non_heading = "####### And this is not"
        self.assertEqual(block_to_block_type(heading_1), block_type_heading)
        self.assertEqual(block_to_block_type(heading_2), block_type_heading)
        self.assertEqual(block_to_block_type(non_heading), block_type_paragraph)
        
    def test_code(self):
        code = "```This is code```"
        non_code = "This ```is``` a paragraph"
        self.assertEqual(block_to_block_type(code), block_type_code)
        self.assertEqual(block_to_block_type(non_code), block_type_paragraph)
        
    def test_quote(self):
        quote = ">This is a quote\n>spanning multiple lines\n> some of which start with a with a whitespace"
        self.assertEqual(block_to_block_type(quote), block_type_quote)
        
    def test_quote_missing_character(self):
        non_quote = ">This is a quote\n>spanning multiple lines\nbut the last line is missing the '>' character"
        self.assertEqual(block_to_block_type(non_quote), block_type_paragraph)
        
    def test_ul(self):
        ul_1 = "* this is an\n* unordered list\n- with both delimeters present"
        ul_2 = "- this is an\n* unordered list\n- with both delimeters present"
        self.assertEqual(block_to_block_type(ul_1), block_type_ul)
        self.assertEqual(block_to_block_type(ul_2), block_type_ul)
        
    def test_ul_missing_character(self):
        non_ul = "* This is an\n* unordered list\n with one line missing the leading '*' character"
        self.assertEqual(block_to_block_type(non_ul), block_type_paragraph)
        
    def test_ol(self):
        ol = "1. this\n2. is\n3. an ordered list"
        self.assertEqual(block_to_block_type(ol), block_type_ol)
        
    def test_ol_wrong_order(self):
        non_ol = "1. This\n3. is not\n2. an ordered list"
        self.assertEqual(block_to_block_type(non_ol), block_type_paragraph)
    
    def test_ol_missing_character(self):
        non_ol = "1. This\n2. is not\n. an ordered list"
        self.assertEqual(block_to_block_type(non_ol), block_type_paragraph)
        
    def test_ol_missing_new_line(self):
        non_ol = "1. This 2. is not\n3. an ordered list"
        self.assertEqual(block_to_block_type(non_ol), block_type_paragraph)

    def test_ordinary_paragraph(self):
        paragraph = "This is just a paragraph"
        self.assertEqual(block_to_block_type(paragraph), block_type_paragraph)
        