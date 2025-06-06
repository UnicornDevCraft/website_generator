from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown import markdown_to_blocks, text_to_textnodes
from textnode import text_node_to_html_node


def block_type_to_tag(block_type, text):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return f"h{text.split()[0].count("#")}"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.CODE:
            return "code"
        case BlockType.OR_LIST:
            return "ol"
        case BlockType.UN_LIST:
            return "ul"
        
        case _:
            return
        
def clean_up_markers(block, block_type):
    match block_type:
        case BlockType.CODE:
            return block.strip("```").lstrip("\n")
        case BlockType.HEADING:
            num_hashes = block.split()[0].count("#")
            to_remove = "#" * num_hashes
            return block.lstrip(to_remove).strip()
        case BlockType.QUOTE:
            new_lines = [line.lstrip("> ") for line in block.splitlines()]
            return " ".join(new_lines)
        case BlockType.PARAGRAPH:
            return " ".join(block.splitlines())
        case BlockType.OR_LIST:
            new_lines = [line.lstrip(f"{i+1}. ") for i, line in enumerate(block.splitlines())]
            return "\n".join(new_lines)
        case BlockType.UN_LIST:
            new_lines = [line.lstrip("- ") for line in block.splitlines()]
            return "\n".join(new_lines)
            
        case _:
            return block

def block_to_html_nodes(tag, block, block_type):
    new_nodes = []
    clean_block = clean_up_markers(block, block_type)
    if block_type == BlockType.CODE:
            return [ParentNode("pre", [LeafNode(tag, clean_block)])]
    html_nodes = [text_node_to_html_node(node) for node in text_to_textnodes(clean_block)]
    if all(node.tag == "img" for node in html_nodes):
        for node in html_nodes:
            new_nodes.append(LeafNode("img", None, node.props))
        return new_nodes
    if len(html_nodes) == 1 and block_type != BlockType.OR_LIST and block_type != BlockType.UN_LIST:
        return [LeafNode(tag, clean_block)]
    if block_type == BlockType.HEADING or block_type == BlockType.PARAGRAPH or block_type == BlockType.QUOTE:
        return [ParentNode(tag, html_nodes)]
    if block_type == BlockType.OR_LIST or block_type == BlockType.UN_LIST:
        child_nodes = []
        for line in clean_block.splitlines():
            children = [text_node_to_html_node(node) for node in text_to_textnodes(line)]
            if len(children) == 1:
                child_nodes.append(LeafNode("li", line))
            else:
                child_nodes.append(ParentNode("li", children))
        return [ParentNode(tag, child_nodes)]
    

def markdown_to_html_node(markdown):
    if markdown:
        blocks = markdown_to_blocks(markdown)
        html_nodes = []
        for block in blocks:
            block_type = block_to_block_type(block)
            tag = block_type_to_tag(block_type, block)
            nodes = block_to_html_nodes(tag, block, block_type)
            if nodes:
                html_nodes.extend(nodes)
            #html_for_block = [node.to_html() for node in nodes]
            #html_code += "\n".join(html_for_block)
        return ParentNode("div", html_nodes)
    return HTMLNode()
        