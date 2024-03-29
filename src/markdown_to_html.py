from block_markdown import *

def markdown_to_html_node(markdown):
    return ParentNode("div", [block_to_html_node(block, block_to_block_type(block)) for block in markdown_to_blocks(markdown)])