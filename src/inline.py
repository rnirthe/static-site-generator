import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_node = old_node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("Wrong number of delimiters")
        for i in range(len(split_node)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.TEXT))
            elif i % 2 == 1:
                new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)", text)


def split_nodes_link(nodes):
    results = []
    for node in nodes:
        new_nodes = []
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        extracted_links = []
        for e in extract_markdown_links(node.text):
            extracted_links.append((f"[{e[0]}]({e[1]})", e))
        if len(extracted_links) == 0:
            results.append(node)
            continue
        temp_text = node.text[:]
        for link in extracted_links:
            split_node = temp_text.split(link[0], 1)
            if split_node[0] != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
            new_nodes.append(TextNode(link[1][0], TextType.LINK, link[1][1]))
            temp_text = split_node[1]
        if split_node[1] != "":
            new_nodes.append(TextNode(split_node[1], TextType.TEXT))
        results.extend(new_nodes)
    return results


def split_nodes_image(nodes):
    results = []
    for node in nodes:
        new_nodes = []
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        extracted_images = []
        for e in extract_markdown_images(node.text):
            extracted_images.append((f"![{e[0]}]({e[1]})", e))
        if len(extracted_images) == 0:
            results.append(node)
            continue
        temp_text = node.text[:]
        for image in extracted_images:
            split_node = temp_text.split(image[0], 1)
            if split_node[0] != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
            new_nodes.append(TextNode(image[1][0], TextType.IMAGE, image[1][1]))
            temp_text = split_node[1]
        if split_node[1] != "":
            new_nodes.append(TextNode(split_node[1], TextType.TEXT))
        results.extend(new_nodes)
    return results


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    bold_filtered = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    italic_filtered = split_nodes_delimiter(bold_filtered, "_", TextType.ITALIC)
    code_filtered = split_nodes_delimiter(italic_filtered, "`", TextType.CODE)
    link_filtered = split_nodes_link(code_filtered)
    image_filtered = split_nodes_image(link_filtered)
    return image_filtered
