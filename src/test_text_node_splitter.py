import unittest
from textnode import TextNode, TextType
from text_node_splitter import split_nodes_delimiter

class TestTextNodeSplitter(unittest.TestCase):
    def test_split_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    def test_split_multiple_delimiters(self):
        node = TextNode("Hello `code` world `code2`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[3].text, "code2")

    def test_bold_delimiter(self):
        node = TextNode("Hello **bold** text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_non_text_node(self):
        node = TextNode("**bold text**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "**bold text**")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_unmatched_delimiter(self):
        node = TextNode("Hello `world", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_empty_delimiter_content(self):
        node = TextNode("Hello `` world", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Hello ")
        self.assertEqual(new_nodes[1].text, " world")

if __name__ == "__main__":
    unittest.main() 