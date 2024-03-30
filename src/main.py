from shutil import rmtree
from os.path import exists
from utils import copy_static_files


def main():
    if exists("public/"):
        rmtree("public/")
    copy_static_files("static/", "public/")
    
main()