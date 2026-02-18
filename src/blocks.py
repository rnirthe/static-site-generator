from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextType, TextNode
from inline import text_to_textnodes
from main import text_node_to_html_node


def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block != "":
            blocks.append(block)
    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    match block[0]:
        case "#":
            return BlockType.HEADING
        case ">":
            return BlockType.QUOTE
        case "`":
            if len(block) >= 7:
                if block[1] == "`" and block[2] == "`" and block[3] == "\n":
                    if block[-1] == "`" and block[-2] == "`" and block[-3] == "`":
                        return BlockType.CODE
            return BlockType.PARAGRAPH
        case "-":
            for line in block.split("\n"):
                line = line.strip()
                if len(line) <= 1:
                    return BlockType.PARAGRAPH
                if line[0] != "-" or block[1] != " ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case "1":
            lines = block.split("\n")
            line_count = 1
            for line in lines:
                line = line.strip()
                if len(line) <= 2:
                    return BlockType.PARAGRAPH
                if line[0] != f"{line_count}" or line[1] != "." or line[2] != " ":
                    return BlockType.PARAGRAPH
                line_count += 1
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        nodes.append(block_to_html_node(block))
    return ParentNode(tag="div", children=nodes)


def block_to_html_node(b):
    block = b[:]
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            block = text_to_textnodes(block)
            parts = []
            for part in block:
                part = text_node_to_html_node(part)
                parts.append(part)
            return ParentNode(tag="p", children=parts)
        case BlockType.HEADING:
            level = 1
            for char in block:
                if char != "#":
                    continue
                level += 1
            block = text_to_textnodes(block)
            parts = []
            for part in block:
                part = text_node_to_html_node(part)
                parts.append(part)
            return ParentNode(tag=f"h{level}", children=parts)
        case BlockType.QUOTE:
            block = text_to_textnodes(block)
            parts = []
            for part in block:
                part = text_node_to_html_node(part)
                parts.append(part)
            return ParentNode(tag="q", children=parts)
        case BlockType.CODE:
            block = block.lstrip("`\n")
            block = block.rstrip("`")
            block = TextNode(block, TextType.CODE)
            block = text_node_to_html_node(block)
            return ParentNode(tag="pre", children=[block])
        case BlockType.UNORDERED_LIST:
            cees = []
            for line in block.split("\n-"):
                line = line.strip()
                line = text_to_textnodes(line)
                parts = []
                for part in line:
                    part = text_node_to_html_node(part)
                    parts.append(part)
                line = ParentNode(tag="li", children=parts)
                cees.append(line)
            return ParentNode(tag="ul", children=cees)

        case BlockType.ORDERED_LIST:
            cees = []
            for line in block.split("\n-"):
                line = line.strip()
                line = text_to_textnodes(line)
                parts = []
                for part in line:
                    part = text_node_to_html_node(part)
                    parts.append(part)
                line = ParentNode(tag="li", children=parts)
                cees.append(line)
            return ParentNode(tag="ol", children=cees)
