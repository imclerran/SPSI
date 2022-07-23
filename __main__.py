#!/usr/bin/env python3

import sys, getopt
from HW5 import *


def readFile(filename):
    with open(filename) as f:
        contents = f.read()
    return contents


def main(argv):
    scope = "static"
    try:
        opts, args = getopt.getopt(argv,"sh",["scope","help"])
    except getopt.GetoptError:
        print('usage: spsi <filename> -s <scope>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: spsi <filename> -s <scope>')
            sys.exit()
        elif opt in ("-s", "--scope"):
            scope = arg
            if scope not in ("static", "dynamic"):
                print("scope not recognized: must be 'static' OR 'dynamic'")
                sys.exit(2)
    if len(args) < 1:
        print('usage: sps <filename> -s <scope>')
        exit(2)
    filename = args[0]
    script = readFile(filename)
    # clearBoth()  #clear both stacks
    # dictstack.append((0,{}))
    interpreter(script, scope)


if __name__ == "__main__":
   main(sys.argv[1:])