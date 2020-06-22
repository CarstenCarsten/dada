#!/usr/bin/env python

import os

def find_files_with_unwanted_chars_in_name(dirName):
    for (dirpath, _, filenames) in os.walk(dirName):
        for complete_file in [os.path.join(dirpath, file) for file in filenames]:
            print(complete_file)
