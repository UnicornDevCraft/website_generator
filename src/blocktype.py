"""This is a file that contains BlockType definition and 
a function to determine the type of the single block of markdown"""

import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UN_LIST = "unordered list"
    OR_LIST = "ordered list"

def block_to_block_type(block):
    lines = block.split("\n")
    
    if "\n" not in block and re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UN_LIST
    if all(re.match(r"^\d+.", line) for line in lines):
        if all(line.split()[0].strip(".") == f"{i + 1}" for i, line in enumerate(lines)):
            return BlockType.OR_LIST
    return BlockType.PARAGRAPH



