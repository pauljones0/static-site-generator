import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

    def test_to_html_with_tag(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_multiple_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        self.assertTrue(
            node.to_html() == '<a href="https://www.google.com" target="_blank">Click me!</a>' or
            node.to_html() == '<a target="_blank" href="https://www.google.com">Click me!</a>'
        )

if __name__ == "__main__":
    unittest.main() 