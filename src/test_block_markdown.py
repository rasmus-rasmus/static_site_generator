import unittest

from block_markdown import *


class TestMarkdownToBlocks(unittest.TestCase):
    def test_three_blocks(self):
        markdown = """## This is a heading
        
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        
        ```This is code```
        """
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, [
            "## This is a heading",
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
            "```This is code```"
        ])
        
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
        

class TestParagraphToHTMLNode(unittest.TestCase):
    def test_paragraph_no_inline(self):
        paragraph = "This is just a paragraph"
        result = paragraph_to_html_node(paragraph)
        result_wrapper_fct = block_to_html_node(paragraph, block_type_paragraph)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("p", [LeafNode(paragraph)])))
        
    def test_paragraph_with_inline(self):
        paragraph = "This is *just* a paragraph"
        result = paragraph_to_html_node(paragraph)
        result_wrapper_fct = block_to_html_node(paragraph, block_type_paragraph)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("p", [LeafNode("This is "), LeafNode("just", "i"), LeafNode(" a paragraph")])))
        
    def test_paragraph_with_link(self):
        paragraph = "[This](https://link.com) is a link"
        result = paragraph_to_html_node(paragraph)
        result_wrapper_fct = block_to_html_node(paragraph, block_type_paragraph)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("p", [LeafNode("This", "a", {"href": "https://link.com"}), LeafNode(" is a link")])))
        
        
class TestHeadingToHTMLNode(unittest.TestCase):
    def test_heading_no_inline(self):
        for i in range(6):
            heading = "#"*(i+1) + " This is a heading"
            result = heading_to_html_node(heading)
            result_wrapper_fct = block_to_html_node(heading, block_type_heading)
            
            self.assertEqual(str(result), str(result_wrapper_fct))
            self.assertEqual(str(result), str(ParentNode(f"h{i+1}", [LeafNode("This is a heading")])))
        
    def test_heading_with_inline(self):
        heading = "### This is a **HEADING**"
        result = heading_to_html_node(heading)
        result_wrapper_fct = block_to_html_node(heading, block_type_heading)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("h3", [LeafNode("This is a "), LeafNode("HEADING", "b")])))
        
    def test_heading_with_link(self):
        heading = "##### [This](https://link.com) is a heading"
        result = heading_to_html_node(heading)
        result_wrapper_fct = block_to_html_node(heading, block_type_heading)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("h5", [LeafNode("This", "a", {"href": "https://link.com"}), LeafNode(" is a heading")])))
        
        
class TestCodeBlockToHTMLNode(unittest.TestCase):
    def test_code(self):
        code = "```This is code blip blop```"
        result = code_block_to_html_node(code)
        result_wrapper_fct = block_to_html_node(code, block_type_code)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("pre", [ ParentNode("code", [LeafNode("This is code blip blop")]) ])))

        
class TestQuoteBlockToHTMLNode(unittest.TestCase):
    def test_quote(self):
        quote = ">This is a\n> multiline quote"
        result = quote_block_to_html_node(quote)
        result_wrapper_fct = block_to_html_node(quote, block_type_quote)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("blockquote", [LeafNode("This is a multiline quote")])))
        
        

class TestUnorderedListToHTMLNode(unittest.TestCase):
    def test_ul_no_inline(self):
        ul = "* This is\n*      an unordered list with excessive whitespaces"    
        result = ul_to_html_node(ul)
        result_wrapper_fct = block_to_html_node(ul, block_type_ul)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("ul", [
            ParentNode("li", [LeafNode("This is")]),
            ParentNode("li", [LeafNode("an unordered list with excessive whitespaces")])
        ])))
        
    def test_ul_with_inline(self):
        ul = "* This is\n* an unordered list with *inline* markdown"    
        result = ul_to_html_node(ul)
        result_wrapper_fct = block_to_html_node(ul, block_type_ul)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("ul", [
            ParentNode("li", [LeafNode("This is")]),
            ParentNode("li", [LeafNode("an unordered list with "), LeafNode("inline", "i"), LeafNode(" markdown")])
        ])))
        
        
class TestOrderedListToHTMLNode(unittest.TestCase):
    def test_ol_no_inline(self):
        ol = "1. This is\n2.      an ordered list with excessive whitespaces"    
        result = ol_to_html_node(ol)
        result_wrapper_fct = block_to_html_node(ol, block_type_ol)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("ol", [
            ParentNode("li", [LeafNode("This is")]),
            ParentNode("li", [LeafNode("an ordered list with excessive whitespaces")])
        ])))
        
    def test_ol_with_inline(self):
        ol = "1. This is\n2. an ordered list with *inline* markdown"    
        result = ol_to_html_node(ol)
        result_wrapper_fct = block_to_html_node(ol, block_type_ol)
        
        self.assertEqual(str(result), str(result_wrapper_fct))
        self.assertEqual(str(result), str(ParentNode("ol", [
            ParentNode("li", [LeafNode("This is")]),
            ParentNode("li", [LeafNode("an ordered list with "), LeafNode("inline", "i"), LeafNode(" markdown")])
        ])))
