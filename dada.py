#!/usr/bin/env python

import argparse
import sys

from localfiles import find_files_with_unwanted_chars_in_name

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
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
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

if __name__ == '__main__':
    DaDa()