from shutil import rmtree
from os.path import exists
from generatepage import generate_page
from utils import copy_static_files


def main():
    if exists("public/"):
        rmtree("public/")
    copy_static_files("static/", "public/")
    generate_page("content/index.md", "template.html", "public/index.html")
    
main()