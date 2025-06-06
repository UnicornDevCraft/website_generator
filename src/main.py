from textnode import TextNode,TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode("a", "Normal text", {"href": "https://www.google.com", "target": "_blank",}),
    ],
)

    print(node.to_html())

main()