import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_image, split_nodes_link

class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_image_basic(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/img.jpg) in it.",
            TextType.NORMAL
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].url, "https://example.com/img.jpg")
        self.assertEqual(new_nodes[2].text, " in it.")

    def test_split_image_multiple(self):
        node = TextNode(
            "![first](one.jpg) ![second](two.jpg)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "first")
        self.assertEqual(new_nodes[1].text, " ")
        self.assertEqual(new_nodes[2].text, "second")

    def test_split_link_basic(self):
        node = TextNode(
            "This is text with a [link](https://example.com) in it.",
            TextType.NORMAL
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].url, "https://example.com")
        self.assertEqual(new_nodes[2].text, " in it.")

    def test_split_link_multiple(self):
        node = TextNode(
            "[first](one.com) [second](two.com)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "first")
        self.assertEqual(new_nodes[1].text, " ")
        self.assertEqual(new_nodes[2].text, "second")

    def test_split_image_non_text_node(self):
        node = TextNode("![image](test.jpg)", TextType.CODE)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_link_non_text_node(self):
        node = TextNode("[link](test.com)", TextType.CODE)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

if __name__ == "__main__":
    unittest.main() 