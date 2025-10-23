import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div", value="test")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="a", value="link", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="img",
            props={
                "src": "/images/photo.jpg",
                "alt": "A photo",
                "class": "thumbnail"
            }
        )
        result = node.props_to_html()
        self.assertIn('src="/images/photo.jpg"', result)
        self.assertIn('alt="A photo"', result)
        self.assertIn('class="thumbnail"', result)
        self.assertTrue(result.startswith(' '))
        self.assertEqual(result.count('="'), 3)


if __name__ == "__main__":
    unittest.main()
