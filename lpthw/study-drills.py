from sys import argv
from os.path import exists
import re

cur = 17

if cur == 17:
    script, from_file, to_file = argv

    # we could do these two on one line, how?
    indata = open(from_file).read()
    open(to_file, 'w').write(indata)


if cur == 16.2:
    ## 16.2
    script, filename = argv

    f = open(filename)
    content = f.read()
    print(content)
