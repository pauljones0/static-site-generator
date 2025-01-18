import unittest
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        text = "This is **text** with an *italic* word"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word")

    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://example.com/img.jpg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[9].text_type, TextType.LINK)

    def test_text_to_textnodes_no_special_text(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is plain text")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL)

    def test_text_to_textnodes_nested_markdown(self):
        text = "This is *italic with a [link](https://boot.dev) inside*"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[1].text, "italic with a ")
        self.assertEqual(nodes[2].text_type, TextType.LINK)

if __name__ == "__main__":
    unittest.main() 