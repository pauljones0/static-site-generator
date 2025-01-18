import unittest
from block_markdown import markdown_to_blocks

class TestBlockMarkdown(unittest.TestCase):
    def test_single_block(self):
        markdown = "This is a single block."
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "This is a single block.")
        
    def test_multiple_blocks(self):
        markdown = """
            This is the first block.

            This is the second block.
            This is still the second block.

            * This is a list block
            * With multiple items
            * In it
            """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "This is the first block.")
        self.assertEqual(blocks[1], "This is the second block.\nThis is still the second block.")
        self.assertEqual(blocks[2], "* This is a list block\n* With multiple items\n* In it")
        
    def test_empty_lines_between_blocks(self):
        markdown = """
First block.


Second block.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "First block.")
        self.assertEqual(blocks[1], "Second block.")
        
    def test_strips_whitespace(self):
        markdown = "  Block with spaces.  \n\n   Another block.\t  "
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "Block with spaces.")
        self.assertEqual(blocks[1], "Another block.")

    def test_markdown_to_html_node(self):
        markdown = """# Header
This is a paragraph with **bold** and *italic* text.

* List item 1
* List item 2

1. Numbered item 1
2. Numbered item 2

> This is a quote
> Multi-line quote
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 5)
        self.assertEqual(blocks[0], "# Header")
        self.assertEqual(blocks[1], "This is a paragraph with **bold** and *italic* text.")
        self.assertEqual(blocks[2], "* List item 1\n* List item 2")
        self.assertEqual(blocks[3], "1. Numbered item 1\n2. Numbered item 2")
        self.assertEqual(blocks[4], "> This is a quote\n> Multi-line quote")

if __name__ == "__main__":
    unittest.main() 