#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

"""Batch Images Processing

Usage:
  concurrent_img_proc.py <source_path> <dest_path>
  concurrent_img_proc.py -h
  concurrent_img_proc.py --version

Reads images and produces processed (e.g. blurred, thumbnail) versions
using concurrent independent processes

Arguments:
    <source_path> source images directory path
    <dest_path>   processed images directory path

Options:
    -h --help          Display this help
    --version          Display version
 
Give us your feedback.
"""

import docopt
import glob
import os
import profile
import sys

from PIL import Image
from PIL import ImageFilter

import concurrent.futures


NB_OF_PROCESSES = 2
new_imgs_path = ""


def make_image_blur(original_img):

    """Creates a blurred of the image

    Args:
        original_img (str): complete file path and name of original image

    Returns:
        The name (str) of the new (blurred) version
    
    The final image will be named "<original_filename>_thumbnail.jpg"""
    
    base_filename, file_extension = os.path.splitext(original_img)
    print("Dirname: '{}'\n"
        "filename: '{}'\n".format(os.path.dirname(original_img), os.path.basename(original_img)))
    blur_filename = f"{new_imgs_path}{os.path.basename(original_img)}_blurred{file_extension}"
    # Create and save thumbnail image
    image = Image.open(original_img)
    blurred = image.filter(ImageFilter.BLUR)
    blurred.save(blur_filename, "JPEG")
    return blur_filename


def launch_process(original_imgs_path):
    """Launchs parallel independent process of image processing tasks

    Args:
        original_imgs_path (str): folder path where original imgs are located

    Returns:
        Nothing
    """

    print(f'Calling {sys.argv[0]} with {NB_OF_PROCESSES} processes')
    print(f'It will process the imgs of "jpg" type located in "{original_imgs_path}"\n')
    with concurrent.futures.ProcessPoolExecutor(NB_OF_PROCESSES) as executor:
        # Loop through all jpeg files in the folder and make a blur for each
        image_list = glob.glob(f"{original_imgs_path}/*.jpg")
        for orig_file, blur_file in zip(image_list, executor.map(make_image_blur, image_list)):
            blur_file = make_image_blur(orig_file)
            print(f"Image '{blur_file}' is ready \n\n")

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='0.1')  # parse arguments based on script docstring     
    new_imgs_path = arguments['<dest_path>']
    launch_process(arguments['<source_path>'])


#   ToDo:
#- Number of processes should be passed as argument
# File extension should be passed as an argument
#- Client should be able to chose among different types of img processing

