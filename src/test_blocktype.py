import unittest

from blocktype import BlockType, block_to_block_type
from markdown import markdown_to_blocks


class TestBlockType(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_none(self):
        md = """
This is one line markdown
"""
        blocks = markdown_to_blocks(md)
        empty_md = ""
        empty_blocks = markdown_to_blocks(empty_md)
        self.assertEqual(blocks, ["This is one line markdown"],)
        self.assertEqual(empty_blocks, [])

    def test_markdown_to_blocks_empty_line(self):
        md = """


This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here


This is the same paragraph on a new line

- This is a list

- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here",
                "This is the same paragraph on a new line",
                "- This is a list",
                "- with items",
            ],
        )

    def test_block_to_block_type_p(self):
        block = "This is a simple paragraph."
        block2 = ""
        result = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, result)
        self.assertEqual("", block2)

    def test_block_to_block_type_h(self):
        heading_blocks = [
            "# This is the h1.",
            "## This is the h2.",
            "### This is the h3.",
            "#### This is the h4.",
            "##### This is the h5.",
            "###### This is the h6.",
        ]

        for block in heading_blocks:
            self.assertEqual(BlockType.HEADING, block_to_block_type(block))

        not_heading = "#This is paragraph."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(not_heading))


    def test_block_to_block_type_code(self):
        block = "```The code line.```"
        block2 = """```This is a code block.
That consists of two lines.```"""
        self.assertEqual(BlockType.CODE, block_to_block_type(block))
        self.assertEqual(BlockType.CODE, block_to_block_type(block2))

    def test_block_to_block_quote(self):
        block = "> This is a quote line."
        block1 = """> This is the qoute
> Block that has a few lines
> Including this one"""
        block2 = """> And this is
        > Just a paragraph, because
        >This line is missing space"""
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block1))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block2))

    def test_block_to_block_un_list(self):
        block = "- This is one item of unordered list"
        block1 = """- This is an unordered list
- That consists of a few
- Lines that are correctly formatted"""
        block2 = """- This is a paragraph
- Because I will format
* - The last line wrong"""
        self.assertEqual(BlockType.UN_LIST, block_to_block_type(block))
        self.assertEqual(BlockType.UN_LIST, block_to_block_type(block1))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block2))

    def test_block_to_block_or_list(self):
        block = "1. This is one item ordered list."
        block1 = """1. This is an ordered list
2. That consists of a few lines
3. That are correctly formatted"""
        block2 = """1. This is the list
3. With a mistake made
2. Intentionally of course"""
        self.assertEqual(BlockType.OR_LIST, block_to_block_type(block))
        self.assertEqual(BlockType.OR_LIST, block_to_block_type(block1))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block2))


if __name__ == "__main__":
    unittest.main()