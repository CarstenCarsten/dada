#!/usr/bin/env python

import argparse
import sys
import config

from localfiles import find_files_with_unwanted_chars_in_name, create_md5_file_list
from adrive import login_and_walk_dir
from comparison import are_all_local_files_in_remote, are_identical, find_needle_in_haystack, are_left_in_right
from encryption import encrypt

class DaDa(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Work with your local files',
            usage='''dada <command> [<args>]

List of dada commands:
   init                     Install the local files in the current folder
   local-unwanted-chars     Search in the current data structure for files
                            with unwanted characters
   local-validate           Check if the local files have the checksum stored
                            locally
   local-md5-filelist       Creates local_filelist.csv with md5 hashes
   remote-create-filelist   Creates adrive_filelist.csv with md5 hashes
   are-local-in-remote      Check if all local files exist in remote
                            This command only checks filelists
   are-left-in-right        Given two filelists, check if all left entries are
                            in the right filelist
   are-identical            Checks whether two filelists contain the same
                            I FORGOT WHY I NEED THIS FUNCTION
   encrypt                  encrypts the files according to the 
                            encryptedfiles.txt
   find-files-in-subfolders Goes through every file in the current directory
                            and checks wether this file exists in another
                            directory, or in that subfolder
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])

        config.read_config()

        dispatchMethod = args.command.replace('-','_')
        if not hasattr(self, dispatchMethod):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, dispatchMethod)()

    def init(self):
        parser = argparse.ArgumentParser(description='Install the local files in the current folder')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (dada) and the subcommand (init)
        args = parser.parse_args(sys.argv[2:])
        print('Running dada init, amend=%s' % args.amend)

    def local_unwanted_chars(self):
        parser = argparse.ArgumentParser(description='Search in the current data structure for files with unwanted characters')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('path')
        args = parser.parse_args(sys.argv[2:])
        print('Running dada local-unwanted-chars, path=%s' % args.path)
        find_files_with_unwanted_chars_in_name(args.path)

    def local_validate(self):
        parser = argparse.ArgumentParser(description='Check if the local files have the checksum stored locally')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('repository')
        args = parser.parse_args(sys.argv[2:])
        print('Running dada local-validate, repository=%s' % args.repository)

    def local_md5_filelist(self):
        parser = argparse.ArgumentParser(description='Create md5 checksums in the local path folder')
        # NOT prefixing the argument with -- means it's not optional
        parser.add_argument('path')#, action='store', dest='folder',
#                    help='name of the folder')
        args = parser.parse_args(sys.argv[2:])
        print('Running dada local-md5-filelist, path=%s' % args.path)
        cleaned_path = args.path.replace('\\','/')
        if not cleaned_path.endswith('/'):
            cleaned_path = f'{cleaned_path}/'
        create_md5_file_list(cleaned_path)

    def remote_create_filelist(self):
        login_and_walk_dir()

    def are_local_in_remote(self):
        are_all_local_files_in_remote()

    def are_identical(self):
        parser = argparse.ArgumentParser(description='Check if two filelists are identical')
        parser.add_argument('leftfile')
        parser.add_argument('rightfile')
        args = parser.parse_args(sys.argv[2:])
        are_identical(args.leftfile, args.rightfile)

    def are_left_in_right(self):
        parser = argparse.ArgumentParser(description='Check if alle entries from the left filelist are in the right')
        parser.add_argument('leftfile')
        parser.add_argument('rightfile')
        args = parser.parse_args(sys.argv[2:])
        are_left_in_right(args.leftfile, args.rightfile)

    def encrypt(self):
        parser = argparse.ArgumentParser(description='Encrypt the files listed in encrypted_files.txt')
        parser.add_argument('path')
        args = parser.parse_args(sys.argv[2:])
        print('Running dada encrypt, path=%s' % args.path)
        cleaned_path = args.path.replace('\\','/')
        if not cleaned_path.endswith('/'):
            cleaned_path = f'{cleaned_path}/'
        encrypt(cleaned_path)

    def find_files_in_subfolders(self):
        parser = argparse.ArgumentParser(description='Takes every file in the needle directory and looks for them in the haystack folder and subfolders')
        parser.add_argument('path_needle')
        parser.add_argument('path_haystack')
        args = parser.parse_args(sys.argv[2:])
        needle_path = args.path_needle.replace('\\','/')
        haystack_path = args.path_haystack.replace('\\','/')
        if not needle_path.endswith('/'):
            needle_path = f'{needle_path}/'
        if not haystack_path.endswith('/'):
            haystack_path = f'{haystack_path}/'


if __name__ == '__main__':
    DaDa()
