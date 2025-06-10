"""This file contains functions that work with the raw markdown"""

import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid markdown syntax")
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text_parts = old_node.text.split(delimiter)
        for index, part in enumerate(text_parts):
            if index % 2 == 0:
                text_node = TextNode(part, TextType.TEXT)
            elif index % 2 != 0:
                text_node = TextNode(part, text_type)
            if len(part) > 0:
                new_nodes.append(text_node)
            
    return new_nodes

def extract_markdown_images(text):
    result = []
    alt_text = re.findall(r"(\!\[.*?\])", text)
    links = re.findall(r"(\(.*?\))", text)
    new_alt_text = [alt.strip("![").strip("]") for alt in alt_text]
    new_links = [link.strip("(").strip(")") for link in links]
    result = list(zip(new_alt_text, new_links))
    return result

def extract_markdown_links(text):
    result = []
    anchor_text = re.findall(r"(\[.*?\])", text)
    urls = re.findall(r"(\(.*?\))", text)
    new_anchor_text = [text.strip("[").strip("]") for text in anchor_text]
    new_urls = [url.strip("(").strip(")") for url in urls]
    result = list(zip(new_anchor_text, new_urls))
    return result

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if re.findall(r"(\!\[.*?\])", old_node.text) and re.findall(r"(\(.*?\))", old_node.text):
            text_parts = old_node.text.split("!")
            if len(text_parts[0]) > 0:
                text_node = TextNode(text_parts[0], TextType.TEXT)
                new_nodes.append(text_node)
            for index, part in enumerate(text_parts):
                if ")" in part:
                    image_details = extract_markdown_images(f"!{part}")
                    if image_details:
                        new_nodes.append(TextNode(image_details[0][0], TextType.IMAGE, image_details[0][-1]))
                        info = part.split(")", maxsplit=1)
                        if len(info[-1]) > 0:
                            new_nodes.append(TextNode(info[-1], TextType.TEXT))
        else:
            new_nodes.append(old_node)
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if re.findall(r"(\[.*?\])", old_node.text) and re.findall(r"(\(.*?\))", old_node.text):
            text_parts = old_node.text.split("[")
            if len(text_parts[0]) > 0:
                text_node = TextNode(text_parts[0], TextType.TEXT)
                new_nodes.append(text_node)
            for index, part in enumerate(text_parts):
                if ")" in part:
                    link_details = extract_markdown_links(f"[{part}")
                    if link_details:
                        new_nodes.append(TextNode(link_details[0][0], TextType.LINK, link_details[0][-1]))
                        info = part.split(")", maxsplit=1)
                        if len(info[-1]) > 0:
                            new_nodes.append(TextNode(info[-1], TextType.TEXT))
        else:
            new_nodes.append(old_node)
            
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(split_nodes_image(new_nodes))
    return new_nodes


def markdown_to_blocks(markdown):
    blocks = []
    parts = markdown.split("\n\n")
    for part in parts:
        new_part = part.strip("\n").strip()
        if len(new_part) > 0:
            blocks.append(new_part)

    return blocks

def extract_title(markdown):
    title = ""
    for line in markdown.splitlines():
        if re.match(r"\#\s.+?", line):
            title = " ".join(line.split()[1:])
    if not title:
        raise Exception("No title was found!")
    
    return title