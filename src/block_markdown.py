from textnode import *

def markdown_to_blocks(markdown):
    blocks_with_internal_whitespaces = [block.strip() for block in filter(lambda a: len(a) > 0, markdown.split("\n\n"))]
    return ["\n".join([line.strip() for line in block.split("\n")]) for block in blocks_with_internal_whitespaces]