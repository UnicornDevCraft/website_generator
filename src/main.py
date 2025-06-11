"""This is the main file which is ran using ./main.sh.
It has the way to copy files from static folder and generate html pages from
the markdown files in the content folder to public folder."""

import os
import shutil
import sys

from markdown import extract_title
from md_to_html import markdown_to_html_node
from textnode import TextNode,TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def copy_to_public(path_from, path_to):
    print(f"Let's copy from {path_from} to {[path_to]}")
    if os.path.exists(path_to):
        print(f"Removing {path_to}")
        try:
            shutil.rmtree(path_to)
        except FileNotFoundError:
            print("Directory not found.")
        except PermissionError:
            print("Permission denied.")

    what_to_copy = os.listdir(path_from)
    print(f"The contents of the static folder: {what_to_copy}")
    
    if not os.path.exists(path_to):
        print(f"Creating {path_to}")
        os.mkdir(path_to)

    for file in what_to_copy:
        to_copy = os.path.join(path_from, file)
        where_to_copy = os.path.join(path_to, file)
        if os.path.isfile(to_copy):
            print(f"Copying {file} to {path_to}")
            try:
                shutil.copy(to_copy, where_to_copy)
                print(f"{file} was successfully copied!")
            except FileNotFoundError:
                print("The file was not found!")
            except PermissionError:
                print("Permission denied.")
        else:
            copy_to_public(to_copy, where_to_copy)
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        markdown = md_file.read()

    with open(template_path) as temp_file:
        template = temp_file.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    new_html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    new_html_page = new_html_page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as dest_file:
        dest_file.write(new_html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.isfile(dir_path_content):
        html_extension = dest_dir_path.replace("md", "html")
        generate_page(dir_path_content, template_path, html_extension, basepath)
    else:
        files_to_generate = os.listdir(dir_path_content)
        for file in files_to_generate:
            file_from = os.path.join(dir_path_content, file)
            file_to = os.path.join(dest_dir_path, file)
            if os.path.isdir(file_from) and not os.path.exists(file_to):
                os.mkdir(file_to)
            generate_pages_recursive(file_from, template_path, file_to, basepath)


def main():
    args = sys.argv
    if len(args) <= 1:
        basepath = "/"
    elif len(args) >= 2:
        basepath = args[1]
    path_from = "static"
    path_to = "docs"
    copy_to_public(path_from, path_to)
    dir_path_content = "content"
    template_path = "template.html"
    dest_dir_path = "docs"
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)
    print(basepath)
main()