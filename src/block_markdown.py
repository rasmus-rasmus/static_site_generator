from textnode import *

from re import split as resplit

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul= "unordered list"
block_type_ol = "ordered list"

def markdown_to_blocks(markdown):
    markdown = "".join(resplit(r" {2,}", markdown)) # Remove excessive internal whitespaces
    return [block.strip() for block in filter(lambda a: len(a) > 0, resplit(r"\n{2,}", markdown))]


def block_to_block_type(block):
    # Heading
    if block[0] == "#":
        index = 1
        while block[index] == "#":
            index += 1
        if index < 5 and block[index] == " ":
            return block_type_heading
        else:
            return block_type_paragraph
    
    # code block
    if block[0:3] == "```" and block[-3:] == "```":
        return block_type_code
    
    lines = block.split("\n")
    # ordered list
    if lines[0][0] == "1" and lines[0][1] == "." and lines[0][2] == " ":
        for index in range(1, len(lines)):
            if lines[index][0] != str(index+1) or lines[index][1] != "." or lines[index][2] != " ":
                return block_type_paragraph
        return block_type_ol
    
    # unordered list
    if (lines[0][0] == "*" or lines[0][0] == "-") and lines[0][1] == " ":
        for index in range(1, len(lines)):
            if (lines[index][0] != "*" and lines[index][0] != "-") or lines[index][1] != " ":
                return block_type_paragraph
        return block_type_ul
    
    # quote
    if lines[0][0] == ">":
        for index in range(1, len(lines)):
            if lines[index][0] != ">":
                return block_type_paragraph
        return block_type_quote
    
    # paragraph
    return block_type_paragraph