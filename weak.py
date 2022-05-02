#!/usr/bin/python3
from parser.weakmatching import WeakMatchingParser
from parser.parserutils import open_files



if __name__ == "__main__":
    verbose = True
    config, target = open_files("test/cfg.txt", "test/weak.txt")
    parser = WeakMatchingParser(config, target, verbose)
    parser.parse()