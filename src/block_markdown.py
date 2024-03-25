from textnode import *

from re import split as resplit

def markdown_to_blocks(markdown):
    markdown = "".join(resplit(r" {2,}", markdown)) # Remove excessive internal whitespaces
    return [block.strip() for block in filter(lambda a: len(a) > 0, resplit(r"\n{2,}", markdown))]