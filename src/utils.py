from os import path, mkdir, listdir
from shutil import copy
import re


def copy_static_files(src, dst):
    if not path.exists(src):
        raise ValueError("Invalid path")
    if not path.exists(dst):
        mkdir(dst, 0o777)
                
    print(f"Copying content of {src}:")
    
    for item in listdir(src):
        item_path = path.join(src, item)
        if path.isfile(item_path):
            copy(item_path, path.join(dst, item))
            print(f"\t* {item_path} -> {path.join(dst, item)}")
        else:
            copy_static_files(item_path, path.join(dst, item))
            
            
def extract_title(markdown):
    pattern = re.compile(r"(?<!\S)# ")
    matches = pattern.search(markdown)
    if not matches:
        raise ValueError("No title found")
    
    title_begin_index = matches.end()
    title_end_index = markdown.find("\n\n", matches.start())
    if title_end_index < 0:
        title_end_index = len(markdown)
    if pattern.search(markdown, title_begin_index):
        raise ValueError("Found more than one title")
    
    return " ".join(markdown[title_begin_index: title_end_index].split("\n"))