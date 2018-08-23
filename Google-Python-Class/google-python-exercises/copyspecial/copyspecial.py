#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
The copyspecial.py program takes one or more directories as its arguments.
We'll say that a "special" file is one where the name contains the pattern __w__ somewhere,
where the w is one or more word chars. The provided main()
includes code to parse the command line arguments, but the rest is up to you.
Write functions to implement the features below and modify main() to call your functions.

Suggested functions for your solution(details below):

get_special_paths(dir) -- returns a list of the absolute paths of the special files in the given directory
copy_to(paths, dir) given a list of paths, copies those files into the given directory
zip_to(paths, zippath) given a list of paths, zip those files up into the given zipfile

Part A (manipulating file paths)
Gather a list of the absolute paths of the special files in all the directories.
In the simplest case, just print that list (here the "." after the command
is a single argument indicating the current directory). Print one absolute path per line.

We'll assume that names are not repeated across the directories
(optional: check that assumption and error out if it's violated).

Part B (file copying)
If the "--todir dir" option is present at the start of the command line,
do not print anything and instead copy the files to the given directory,
creating it if necessary. Use the python module "shutil" for file copying.

Part C (calling an external program)
If the "--tozip zipfile" option is present at the start of the command line,
run this command: "zip -j zipfile <list all the files>".
This will create a zipfile containing the files. Just for fun/reassurance,
also print the command line you are going to do first (as shown in lecture).
(Windows note: windows does not come with a program to produce
standard .zip archives by default, but you can get download the free and open
zip program from www.info-zip.org.)

If the child process exits with an error code, exit with an error code and
print the command's output. Test this by trying to write a zip file to a directory that does not exist.

"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(paths):
    special_paths = []
    files = os.listdir(paths)
    for file in files:
        if re.search('__\w+__',file):
            # this gives the absolute path
            #print(os.path.join(os.path.abspath(cur_path),file))
            special_paths.append(os.path.join(os.path.abspath(cur_path),file))
    return special_paths

def copy_to(paths, dir):
    # check to see if the directory exists, if not, make it.
    if not os.path.exists(dir):
        os.mkdir(dir)
    for files in paths:
        # copy the files
        shutil.copy(files, dir)
    return

def zip_to(paths, zipfilepath):
    filelist = ' '.join(paths)
    cmd = 'zip -j %s %s' % (zipfilepath, filelist)
    print(cmd)
    os.system(cmd)
    return


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  special_paths = get_special_paths(args)
  if todir:
    copy_to(special_paths, todir)
  if tozip:
    zip_to(special_paths,tozip)
  if not tozip and not todir:
    print(special_paths)


if __name__ == "__main__":
  main()
