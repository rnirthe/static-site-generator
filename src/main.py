import os
import shutil
from blocks import markdown_to_html_node


def main():
    my_copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        file_path = f"{dir_path_content}/{file}"
        dest_path = f"{dest_dir_path}/{file}"
        if os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, dest_path)
        elif len(file) > 3 and file[-3:] == ".md":
            generate_page(file_path, template_path, f"{dest_path[:-3]}.html")


def my_copy(src, dest):
    shutil.rmtree(f"./{dest}")
    os.mkdir(dest)
    print(f"Copying files to {dest}...")
    for file in os.listdir(src):
        if os.path.isdir(f"{src}/{file}"):
            os.mkdir(f"{dest}/{file}")
            my_copy(f"{src}/{file}", f"{dest}/{file}")
        else:
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
