import unittest
from block_markdown import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello, World!"
        self.assertEqual(extract_title(markdown), "Hello, World!")

    def test_extract_title_with_spaces(self):
        markdown = "#    Lots of spaces    "
        self.assertEqual(extract_title(markdown), "Lots of spaces")

    def test_extract_title_multiline(self):
        markdown = """# The Title
        
        Some content
        ## Subtitle
        More content"""
        self.assertEqual(extract_title(markdown), "The Title")

    def test_extract_title_no_title(self):
        markdown = "No title here\nJust content"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_wrong_level(self):
        markdown = "## Not a level 1 heading"
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main() 