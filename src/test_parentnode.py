import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_node_basic(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ]
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]
                )
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text</p><p><i>italic text</i>Normal text</p></div>"
        )

    def test_parent_node_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "Hello, World!")],
            {"class": "greeting", "id": "message"}
        )
        self.assertTrue(
            node.to_html() == '<div class="greeting" id="message">Hello, World!</div>' or
            node.to_html() == '<div id="message" class="greeting">Hello, World!</div>'
        )

    def test_no_tag_raises_error(self):
        node = ParentNode(None, [LeafNode(None, "Hello, World!")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

if __name__ == "__main__":
    unittest.main() 