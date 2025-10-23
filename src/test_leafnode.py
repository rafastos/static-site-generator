import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_no_props(self):
        node = LeafNode(tag="p", value="Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_to_html_with_props(self):
        node = LeafNode(tag="a", value="Click me", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me</a>')

    def test_to_html_multiple_props(self):
        node = LeafNode(
            tag="img",
            value="",
            props={"src": "/image.jpg", "alt": "An image"}
        )
        result = node.to_html()

        self.assertIn('src="/image.jpg"', result)
        self.assertIn('alt="An image"', result)
        self.assertTrue(result.startswith("<img"))
        self.assertTrue(result.endswith("></img>"))

    def test_to_html_no_value_raises(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("leaf nodes must have a value", str(context.exception).lower())


if __name__ == "__main__":
    unittest.main()
