#!/usr/bin/python3
from parser.strictmatching import StrictMatchingParser
from parser.parserutils import open_files



if __name__ == "__main__":
    verbose = True
    config, target = open_files("test/cfg.txt", "test/strict.txt")
    parser = StrictMatchingParser(config, target, verbose)
    parser.parse()