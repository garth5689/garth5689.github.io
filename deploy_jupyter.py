#!/usr/bin/env python3

import subprocess
import argparse
from os import path, listdir
import shutil
import re

# nbconvert notebook
# move support files
# remove first line
# replace picture file names

# should be run from website root


image_path_format = "{{{{ site.baseurl }}}}/{0}/"
image_re = re.compile(".*\.(jpe?g|gif|png)$")
tex_re = re.compile(".*\.tex$")

def print_subprocess(args):
    print("running: {}".format(' '.join(args)))


def main(notebook, website_markdown_location, website_image_path):
    # run the actual conversion from the notebook to .md file
    convert_args = ["jupyter", "nbconvert", "--to", "markdown", notebook]
    print_subprocess(convert_args)
    convert = subprocess.run(convert_args, stdout=subprocess.PIPE)

    if convert.returncode == 0:
        # only if the conversion was successful
        website_image_path = website_image_path.rstrip("/")

        notebook_path, notebook_file = path.split(notebook)
        notebook_name, notebook_ext  = path.splitext(notebook_file)
        supporting_files = "{}_files".format(notebook_name)

        markdown_file = notebook_name + ".md"

        # regenerate any tex files (for images)
        for file_name in listdir(notebook_path):
            if tex_re.match(file_name):
                tex_name, tex_ext = notebook_name, notebook_ext  = path.splitext(file_name)
                pdflatex_args = ["pdflatex", "--output-directory",notebook_path, path.join(notebook_path,file_name)]
                print_subprocess(pdflatex_args)
                subprocess.run(pdflatex_args, stdout=subprocess.PIPE)

                convert_pdf_args = ["convert",
                               "-density",
                               "300",
                               "{}.pdf".format(path.join(notebook_path,tex_name)),
                               "{}.png".format(path.join(notebook_path,tex_name))]
                print_subprocess(convert_pdf_args)
                subprocess.run(convert_pdf_args, stdout=subprocess.PIPE)


        with open(path.join(notebook_path, markdown_file), 'r') as md_file:
            md_contents = md_file.read()

            # create the url to place in front of image files to redirect them
            # to the correct location
            image_url_substitution = image_path_format.format(website_image_path)

            # remove all blank lines from beginning of file
            md_contents = re.sub(r"^\s*","",md_contents)

            #redirect any files that were generated into supporting files
            md_contents = re.sub("\((?={})".format(supporting_files),
                                 "({}".format(image_url_substitution),
                                 md_contents)

            # redirect any images that were imported directly from the folder
            md_contents = re.sub(r"!\[(.*?)\]\((.*?)\)",
                                 r"![\1]({}\2)".format(image_url_substitution),
                                 md_contents)

        # move any images in the folder to the website images folder
        for file_name in listdir(notebook_path):
            if image_re.match(file_name):
                shutil.copy(path.join(notebook_path,file_name), website_image_path)

        # remove the old supporting files folder supporting files folder
        if (path.exists(path.join(website_image_path, supporting_files))):
            shutil.rmtree(path.join(website_image_path, supporting_files))

        # move the supporting files folder to the website images folder
        try:
            shutil.move(path.join(notebook_path,supporting_files), website_image_path)
        except FileNotFoundError:
            #that's ok that means there's no files to find.
            pass

        # write new md contents with updated image paths
        # should be last to trigger refresh
        with open(path.join(notebook_path, markdown_file), 'w') as md_file:
            md_file.write(md_contents)

        # markdown file is modified in the notebook directory
        # then copied over to prevent premature rendering in jekyll
        if path.exists(website_markdown_location):
            shutil.copy(path.join(notebook_path, markdown_file),
                        website_markdown_location)
        else:
            print("website location for markdown file does not exist")
            return 1

    else:
        print("markdown generation not successful")
        return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('notebook', type=str)
    parser.add_argument('website_markdown_location', type=str)
    parser.add_argument('website_image_path', type=str)
    args = parser.parse_args()

    main(args.notebook, args.website_markdown_location, args.website_image_path)
