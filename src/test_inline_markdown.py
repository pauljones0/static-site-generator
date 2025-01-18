import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links

class TestInlineMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_links_with_images(self):
        text = "This is text with an ![image](https://example.com/img.jpg) and a [link](https://example.com)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("link", "https://example.com")])

    def test_extract_markdown_images_with_multiple_brackets(self):
        text = "![alt [with brackets]](https://example.com/img.jpg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("alt [with brackets]", "https://example.com/img.jpg")])

if __name__ == "__main__":
    unittest.main() 