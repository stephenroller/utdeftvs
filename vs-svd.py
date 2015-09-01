#!/usr/bin/env python
import sys
import argparse

def main():
    parser = argparse.ArgumentParser('Dimensionality reduces a space using the SVD')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')
    args = parser.parse_args()

if __name__ == '__main__':
    main()
