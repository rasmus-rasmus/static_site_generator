from shutil import rmtree
from os.path import exists
from generatepage import generate_pages_recursively
from utils import copy_static_files


def main():
    if exists("public/"):
        rmtree("public/")
    copy_static_files("static/", "public/")
    generate_pages_recursively("content/", "template.html", "public/")
    
main()