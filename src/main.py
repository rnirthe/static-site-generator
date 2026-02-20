import os
import shutil
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import markdown_to_html_node


def main():
    # new_node = TextNode("dummy", TextType.TEXT)
    # print(new_node)
    my_copy("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_page(
        "content/blog/glorfindel/index.md",
        "template.html",
        "public/blog/glorfindel/index.html",
    )
    generate_page(
        "content/blog/majesty/index.md",
        "template.html",
        "public/blog/majesty/index.html",
    )
    generate_page(
        "content/blog/tom/index.md", "template.html", "public/blog/tom/index.html"
    )


def my_copy(src, dest):
    shutil.rmtree(f"./{dest}")
    os.mkdir(dest)
    print(f"Copying files to {dest}...")
    for file in os.listdir(src):
        print(file)
        if os.path.isdir(f"{src}/{file}"):
            print("isdir somehow", file)
            os.mkdir(f"{dest}/{file}")
            my_copy(f"{src}/{file}", f"{dest}/{file}")
        else:
            print("not a dir", file)
            shutil.copy(f"{src}/{file}", f"{dest}/{file}")


def extract_title(markdown):
    for line in markdown.split("\n"):
        line = line.strip()
        if len(line) > 2 and line[0] == "#" and line[1] != "#":
            return line[2:]
    raise Exception("No title found.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    content_md = open(from_path, "r").read()
    template = open(template_path, "r").read()
    html = markdown_to_html_node(content_md).to_html()
    title = extract_title(content_md)
    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    file = open(dest_path, "w")
    file.write(result)
    file.close()


main()
