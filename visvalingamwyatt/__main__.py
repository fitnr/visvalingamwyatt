# This file is part of visvalingamwyatt.
# https://github.com/fitnr/visvalingamwyatt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, 2017, fitnr <contact@fakeisthenewreal.org>

import argparse
from .simplify import simplify

def main():
    parser = argparse.ArgumentParser('simplify', description='Simplify geospatial data using with the Visvalingam-Wyatt algorithm')
    parser.add_argument('input', default='/dev/stdin', help='geodata file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--threshold', type=float, metavar='float')
    group.add_argument('-n', '--number', type=int, metavar='int')
    group.add_argument('-r', '--ratio', type=float, metavar='float', help='fraction of points to keep')

    parser.add_argument('-o', '--output', metavar='file', default='/dev/stdout')

    args = parser.parse_args()

    if args.input == '-':
        args.input = '/dev/stdin'

    if args.output == '-':
        args.output = '/dev/stdout'

    kwargs = {}

    if args.number:
        kwargs['number'] = args.number

    elif args.threshold:
        kwargs['threshold'] = args.threshold

    else:
        kwargs['ratio'] = args.ratio or 0.90

    simplify(args.input, args.output, **kwargs)

if __name__ == '__main__':
    main()
