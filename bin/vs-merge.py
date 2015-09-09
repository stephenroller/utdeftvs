#!/usr/bin/env python

#!/usr/bin/env python
import sys
import argparse

import bz2

class MagicFile(object):
    def __init__(self, filename):
        self.filename = filename
        if filename.endswith('.bz2'):
            self.handle = bz2.BZ2File(filename)
        else:
            self.handle = open(filename)
        self.peek = None
        self.pop()

    def pop(self):
        retval = self.peek
        try:
            self.peek = self.handle.next().strip()
        except StopIteration:
            self.peek = None
        return retval

    def close(self):
        self.handle.close()

    def __repr__(self):
        return  self.filename + ": " + self.peek

def magic_iterator(magic_files):
    while magic_files:
        mini = magic_files[0].peek
        argmin = magic_files[0]
        for mf in magic_files[1:]:
            if mf.peek < mini:
                mini = mf.peek
                argmin = mf
        retval = argmin.pop()
        if retval:
            yield retval

        if argmin.peek is None:
            argmin.close()
            magic_files.remove(argmin)

def main():
    parser = argparse.ArgumentParser('Reads each of the files, outputting the next line alphabetically from each file.')
    parser.add_argument('inputs', nargs='+')
    args = parser.parse_args()

    magic_files = [MagicFile(file) for file in args.inputs]

    for line in magic_iterator(magic_files):
        print line


if __name__ == '__main__':
    main()
