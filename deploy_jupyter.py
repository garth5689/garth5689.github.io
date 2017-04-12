#!/usr/bin/env python3

import subprocess
import argparse
from os import path
import shutil
import re

# nbconvert notebook
# move support files
# remove first line
# replace picture file names

impage_path_format = "{{{{ site.baseurl }}}}/{0}"

def main(notebook, markdown_location, image_path):
    convert = subprocess.run(["jupyter", "nbconvert", "--to", "markdown", notebook],
                             stdout=subprocess.PIPE)

    #import pdb; pdb.set_trace()
    if convert.returncode == 0:
        image_path = image_path.rstrip("/")

        notebook_path, notebook_file = path.split(notebook)
        notebook_name, notebook_ext  = path.splitext(notebook_file)
        supporting_files = "{}_files".format(notebook_name)

        markdown_file = notebook_name + ".md"

        if path.exists(markdown_location):
            shutil.copy(path.join(notebook_path, markdown_file),
                        markdown_location)

        with open(path.join(markdown_location, markdown_file), 'r') as md_file:
            md_contents = md_file.read()

        # remove all starting blank lines
        md_contents = re.sub(r"^\s*","",md_contents)
        md_contents = re.sub("\((?={})".format(supporting_files),
                             "({{{{ site.baseurl }}}}/{}/".format(image_path),
                             md_contents)

        if (path.exists(path.join(image_path, supporting_files))):
            shutil.rmtree(path.join(image_path, supporting_files))

        try:
            shutil.move(path.join(notebook_path,supporting_files), image_path)
        except FileNotFoundError:
            #that's ok that means there's no files to find.
            pass

        with open(path.join(markdown_location, markdown_file), 'w') as md_file:
            md_file.write(md_contents)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', type=str)
    parser.add_argument('markdown_location', type=str)
    parser.add_argument('image_path', type=str)
    args = parser.parse_args()

    main(args.notebook, args.markdown_location, args.image_path)
