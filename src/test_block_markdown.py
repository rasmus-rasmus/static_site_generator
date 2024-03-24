import unittest

from block_markdown import markdown_to_blocks


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