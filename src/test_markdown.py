import unittest

from md_to_html import markdown_to_html_node
from markdown import extract_title

class TestMarkdownParsing(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )

    def test_blockquote(self):
        md = """
> "This is a blockquote"
> 
> with **bold** and _italic_
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>\"This is a blockquote\"  with <b>bold</b> and <i>italic</i></blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- First item **bold**
- Second item _italic_
- Third item with `code`
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item <b>bold</b></li><li>Second item <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>"
        )

    def test_unordered_list_with_links(self):
        md = """
- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, '<div><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li><li><a href="/blog/majesty">The Unparalleled Majesty of "The Lord of the Rings"</a></li></ul></div>')

    def test_ordered_list(self):
        md = """
1. First item
2. Second item **bold**
3. Third with [link](https://example.com)
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item <b>bold</b></li><li>Third with <a href=\"https://example.com\">link</a></li></ol></div>"
        )

    def test_inline_formatting_in_paragraph(self):
        md = """
A paragraph with **bold**, _italic_, `code`, [link](https://example.com), and ![image](https://example.com/image.png)
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>A paragraph with <b>bold</b>, <i>italic</i>, <code>code</code>, <a href=\"https://example.com\">link</a>, and <img src=\"https://example.com/image.png\" alt=\"image\"></p></div>"
        )

    def test_image_only_block(self):
        md = """
![image](https://example.com/pic.png)
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><img src=\"https://example.com/pic.png\" alt=\"image\"></div>"
        )

    def test_empty_input(self):
        md = ""
        with self.assertRaises(NotImplementedError):
            markdown_to_html_node(md).to_html()

    def test_whitespace_input(self):
        md = "   \n   \n"
        with self.assertRaises(ValueError):
            markdown_to_html_node(md).to_html()

    def test_malformed_markdown(self):
        md = """
This is a paragraph with [broken link](not closed

And an unmatched **bold start

Another _italic
"""
        with self.assertRaises(Exception):
            markdown_to_html_node(md).to_html()

    def test_extract_title(self):
        md = """
# This is the title

## And this is not the title

#

"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")

    def test_extract_title_exception(self):
        md = """
There is no title
## In this markdown
# """
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_no_md(self):
        md = " "
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()