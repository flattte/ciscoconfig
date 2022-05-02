#!/usr/bin/python3
import argparse
from parser.weakmatching import WeakMatchingParser
from parser.parserutils import open_files



if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Check whether cisco running/startup-config file has given attributes",
                                         usage="Create file to check against actual config example:\n    some.txt\n    GigabitEthernet0/0/0 ipv4 192.168.0.1 255.255.255.0")
    arg_parser.add_argument('-c', dest='config', help='path to cisco config file. relative for all strings not starting with valid Windows Disk name or / ~/')
    arg_parser.add_argument('-t', dest='target', help='path to a file with target configuration.')
    arg_parser.add_argument('--verbose',action='store_true', help="Toggle for git diff-like comparasion of config and target configuration")
    args = arg_parser.parse_args()

    config, target = open_files(args.config, args.target)
    parser = WeakMatchingParser(config, target, args.verbose)
    parser.parse()
 

    print(f"Matches found {parser.count} out of {parser.n_of_tokens}")
