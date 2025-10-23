import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_no_tag_raises_error(self):
        child = LeafNode("p", "text")
        node = ParentNode(tag=None, children=[child])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("no tag", str(context.exception).lower())

    def test_no_children_raises_error(self):
        node = ParentNode(tag="div", children=[])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("no children", str(context.exception).lower())

    def test_single_child(self):
        child = LeafNode("span", "Hello")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>Hello</span></div>")

    def test_multiple_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, " and "),
            LeafNode("i", "italic text")
        ]
        parent = ParentNode("p", children)
        expected = "<p><b>Bold text</b> and <i>italic text</i></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_nested_parents_recursion(self):
        innermost = LeafNode("span", "Nested text")
        middle = ParentNode("p", [innermost])
        outer = ParentNode("div", [middle])
        
        expected = "<div><p><span>Nested text</span></p></div>"
        self.assertEqual(outer.to_html(), expected)

    def test_deeply_nested_structure(self):
        # <article>
        #   <div>
        #     <p>
        #       <b>bold</b> normal <i>italic</i>
        #     </p>
        #   </div>
        # </article>
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode(None, " normal ")
        leaf3 = LeafNode("i", "italic")
        p_node = ParentNode("p", [leaf1, leaf2, leaf3])
        div_node = ParentNode("div", [p_node])
        article_node = ParentNode("article", [div_node])
        
        expected = "<article><div><p><b>bold</b> normal <i>italic</i></p></div></article>"
        self.assertEqual(article_node.to_html(), expected)

    def test_parent_with_props(self):
        child = LeafNode("span", "Content")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        result = parent.to_html()
        
        self.assertTrue(result.startswith("<div"))
        self.assertTrue(result.endswith("</div>"))
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        self.assertIn("<span>Content</span>", result)

    def test_mixed_nested_with_props(self):
        # <div class="wrapper">
        #   <p>
        #     <a href="url">link</a>
        #   </p>
        # </div>
        link = LeafNode("a", "link", props={"href": "https://example.com"})
        paragraph = ParentNode("p", [link])
        wrapper = ParentNode("div", [paragraph], props={"class": "wrapper"})
        
        result = wrapper.to_html()
        self.assertIn('<div class="wrapper">', result)
        self.assertIn('<a href="https://example.com">link</a>', result)
        self.assertIn("</div>", result)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
