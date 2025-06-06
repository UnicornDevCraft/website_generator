import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "Link", ["p", "a"], {"href": "https://www.google.com"})
        node1 = HTMLNode("a", "Link", ["p", "a"], {"href": "https://www.google.com"})
        self.assertEqual(node, node1)

    def test_not_eq(self):
        node = HTMLNode("a", "Link", ["p", "a"], {"href": "https://www.google.com"})
        node1 = HTMLNode("p", "Link", ["p", "a"], {"href": "https://www.google.com"})
        node3 = HTMLNode("a", "Anchor", ["p", "a"], {"href": "https://www.google.com"})
        node4 = HTMLNode("a", "Link", ["p", "p"], {"href": "https://www.google.com"})
        node5 = HTMLNode("a", "Link", ["p", "a"], {"href": "http://www.google.com"})
        node6 = HTMLNode("a", "Link", ["p", "a"], {"href": None})
        self.assertNotEqual(node, node1)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        self.assertNotEqual(node, node6)

    def test_none(self):
        node = HTMLNode("a", None, ["p", "a"], {"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, ["p", "a"])
        self.assertEqual(node.props, {"href": "https://www.google.com"})

    def test_html_to_props(self):
        node = HTMLNode("a", "link", ["p"], {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode("a", "link", ["p"], {'href': 'https://www.google.com', 'target': '_blank',})
        self.assertEqual(node.__repr__(), "HTMLNode: a, link, ['p'], {'href': 'https://www.google.com', 'target': '_blank'}")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_none(self):
        node = LeafNode("a", None, {"href": "https://www.google.com", "target": "_blank",})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_eq_parent(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        child_node1 = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node1])
        self.assertEqual(parent_node, parent_node1)

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

    def test_to_html_with_props(self):
        grandchild_node = LeafNode("a", "grandchild", {"href": "https://www.google.com", "target": "_blank",})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), 
            '<div><span><a href="https://www.google.com" target="_blank">grandchild</a></span></div>'
        )

    def test_child_none(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_tag_none(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_not_eq_parent(self):
        grandchild_node = LeafNode("a", "grandchild", {"href": "https://www.google.com", "target": "_blank",})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("a", [child_node])
        self.assertNotEqual(parent_node, parent_node2)

    def test_not_eq_child(self):
        child_node = LeafNode("a", "child", {"href": "https://www.google.com"})
        child_node1 = LeafNode("a", "child", {"href": "https://www.google.com", "target": "_blank",})
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node1])
        self.assertNotEqual(parent_node, parent_node2)