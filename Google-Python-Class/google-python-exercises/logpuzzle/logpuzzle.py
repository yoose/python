#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  hostname = 'developers.google.com'
  #print(hostname)
  f = open(filename, 'ru')
  log = f.readlines()
  urls = []
  url_dict = {}
  for entry in log:
    match = re.search(r'GET (\S*puzzle\S*)', entry)
    if match:
        url = match.group(1)
        urlnew = url.replace('languages/google-python-class','python')
        fullurl = 'https://'+hostname+urlnew
        if not fullurl in urls:
            urls.append(fullurl)
  f.close()
  url_check = re.search(r'\S-\w*-\w*\.jpg',urls[0])
  if url_check:
    tmp_urls = []
    def extract_second_word(url):
        second_word = ''
        match = re.search(r'\S-\w*-(\w*)\.jpg',url)
        if match:
            second_word = match.group(1)
        return second_word
    for url in urls:
        second_word = extract_second_word(url)
        if not second_word in url_dict and second_word:
            url_dict[second_word] = url
    for key in sorted(url_dict.keys()):
        tmp_urls.append(url_dict[key])
    urls = tmp_urls
  else:
    urls.sort()
  return urls

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  if not os.path.exists(dest_dir):
      os.mkdir(dest_dir)
  code = '<html><body>'
  for index, url in enumerate(img_urls):
      local_file = 'img%d.jpg' % index
      urllib.urlretrieve(url,dest_dir+'/'+local_file)
      code += '<img src="%s">' % local_file
  code += "</body></html>"
  output_file = open(dest_dir+'/index.html', 'w')
  output_file.write(code)
  output_file.close()

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
