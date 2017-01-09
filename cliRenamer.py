import argparse
import re
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description="This is a bath renamer",
                                     usage= 'To replace all files with hello with godbye insead: python cliRenamer.py hello godbye')

    parser.add_argument('inString', help='The word to replace')
    parser.add_argument('outString', help='The word to replace it with')

    parser.add_argument('-d', '--duplicate', help='Wheter to duplicate or replace in spot', action='store_true')
    parser.add_argument('-r', '--regex', help='Wheter the patterns are regex or not',
                        action='store_true')
    parser.add_argument('-o', '--out', help='The output location. Default to here')


    args = parser.parse_args()

    print args

if __name__ == '__main__':
    main()

