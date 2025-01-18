import unittest
from block_markdown import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), "paragraph")
        
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("## Heading 2"), "heading")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading")
        # Test invalid headings
        self.assertEqual(block_to_block_type("####### Invalid Heading"), "paragraph")
        self.assertEqual(block_to_block_type("#Not a heading"), "paragraph")
        
    def test_code(self):
        block = "```\ncode block\nmore code\n```"
        self.assertEqual(block_to_block_type(block), "code")
        # Test incomplete code blocks
        self.assertEqual(block_to_block_type("```\ncode block"), "paragraph")
        
    def test_quote(self):
        self.assertEqual(block_to_block_type(">quote"), "quote")
        self.assertEqual(block_to_block_type(">line 1\n>line 2"), "quote")
        # Test invalid quote
        self.assertEqual(block_to_block_type(">line 1\nline 2"), "paragraph")
        
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* item 1\n* item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), "unordered_list")
        # Test invalid lists
        self.assertEqual(block_to_block_type("* item 1\n- item 2"), "paragraph")
        self.assertEqual(block_to_block_type("*invalid"), "paragraph")
        
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second"), "ordered_list")
        # Test invalid ordered lists
        self.assertEqual(block_to_block_type("1. First\n3. Third"), "paragraph")
        self.assertEqual(block_to_block_type("1. First\n2 Second"), "paragraph")

if __name__ == "__main__":
    unittest.main() 