import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

#HTMLNode tests
    def test_stores_tag(self):
        node = HTMLNode("a","hello world", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.tag, "a")
    
    def test_stores_value(self):
        node = HTMLNode("a","hello world", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.value, "hello world")
        
    def test_props(self):
        node = HTMLNode("a","hello world", None, {"href": "https://www.boot.dev"})
        expected = ' href="https://www.boot.dev"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_two_props(self):
        node2 = HTMLNode("a","hello world", None, {"href": "https://www.boot.dev", "img": "https://coderslegacy.com"})
        expected = ' href="https://www.boot.dev" img="https://coderslegacy.com"'
        self.assertEqual(node2.props_to_html(), expected)
    
    def test_no_props(self):
        node0 = HTMLNode("p", "hello world")
        self.assertEqual(node0.props_to_html(), "")

#LeafNode tests
    def test_stores_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
    
    def test_stores_value(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.value, "Hello, world!")
    
    def test_stores_empty_str_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.value, "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a","hello world", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">hello world</a>')
    
    def test_leaf_no_tag(self):
        node = LeafNode(None,"hello world", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), node.value)

    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None, {"href": "https://www.boot.dev"})
            node.to_html()

#ParentNode tests
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
    
    def test_to_html_with_1c_2gc_2ggc(self):
        ggc_node1 = LeafNode("b", "quoicoubeh")
        ggc_node2 = LeafNode("i", "67")
        grandchild_node1 = LeafNode("b", "grandchild")
        grandchild_node2 = ParentNode("span", [ggc_node1, ggc_node2])
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><span><b>quoicoubeh</b><i>67</i></span></span></div>",
        )
    
    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()