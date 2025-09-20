#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def save_homelette_logo():
    """
    This script is to save the Homelette logo image to the project directory.
    The user provided an image of the Homelette logo that needs to be saved as homelette_logo.jpg
    """
    
    print("Please save the Homelette logo image as 'homelette_logo.jpg' in this directory:")
    print(os.getcwd())
    print("\nThe image should be the one you provided showing the charcuterie platter with 'HOMELETTE' branding.")
    print("You can drag and drop the image file into this directory and rename it to 'homelette_logo.jpg'")

if __name__ == "__main__":
    save_homelette_logo()