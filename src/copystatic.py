from os import path, mkdir, listdir
from shutil import copy


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