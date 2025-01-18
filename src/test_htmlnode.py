import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank"
        })
        self.assertTrue(
            node.props_to_html() == ' href="https://www.google.com" target="_blank"' or
            node.props_to_html() == ' target="_blank" href="https://www.google.com"'
        )

    def test_repr(self):
        node = HTMLNode("p", "Hello, World!", None, {"class": "greeting"})
        self.assertEqual(repr(node), "HTMLNode(p, Hello, World!, None, {'class': 'greeting'})")

if __name__ == "__main__":
    unittest.main() 