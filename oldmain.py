#!/usr/bin/python3
import argparse
from parser.weakmatching import *

def open_files(path1, path2):
    assert type(args.config) is str, "Enter a -s flag followed by config path to config file."
    assert type(args.target) is str, "Enter a -t flag followed by config path to config file."
    try:
        file1 = open(path1, 'r')
    except Exception as e:
        exit(f"Exception {e.__class__} occurred while opening {path1}. \n Enter a valid path to a file that exists")

    try:
        file2 = open(path2, 'r')
    except Exception as e:
        exit(f"Exception {e.__class__} occurred while opening {path2}. \n Enter a valid path to a file that exists")

    return file1, file2


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Check whether cisco running/startup-config file has given attributes",
                                         usage="Create file to check against actual config example:\n    some.txt\n    GigabitEthernet0/0/0 ipv4 192.168.0.1 255.255.255.0")
    arg_parser.add_argument('-c', dest='config', help='path to cisco config file. relative for all strings not starting with valid Windows Disk name or / ~/')
    arg_parser.add_argument('-t', dest='target', help='path to a file with target configuration.')
    arg_parser.add_argument('--verbose',action='store_true', help="Toggle for git diff-like comparasion of config and target configuration")
    args = arg_parser.parse_args()

    config, target = open_files(args.config, args.target)
    
    config_tokens = tokenizeConfig(config)   
    target_tokens = [line for line in target.read().splitlines()]

    matches = matchTokens(config_tokens, target_tokens)
    results = getBest(matches)
    # data frame:
    #   result[0]     - metric score
    #   results[1][0] - body of a token
    #   results[1][1] - query

    count = [0]
    for r in results:
        oracle(r, args.verbose, count)

    print(f"Matches {count[0]} out of {len(results)}")
