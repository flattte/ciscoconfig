#!/usr/bin/python3
from ssh.configfdownloader import ConfigDownloader
from parser.strictmatching import StrictMatchingParser
from parser.parserutils import open_files
import argparse


if __name__ == "__main__":
    # example:
    # python3 remote_check.py -c test/cfg.txt -u admin -p secret -ip 192.168.43.32 192.168.43.33
    arg_parser = argparse.ArgumentParser(description="Check whether cisco running/startup-config file has given attributes",
                                         usage="Create file to check against actual config example:\n    some.txt\n    GigabitEthernet0/0/0 ipv4 192.168.0.1 255.255.255.0")
    arg_parser.add_argument('-c', dest='config', help='path to cisco config file. relative for all strings not starting with valid Windows Disk name or / ~/')
    arg_parser.add_argument('-u', dest='username', help='username for cisco device')
    arg_parser.add_argument('-p', dest='password', help='password for cisco device')
    arg_parser.add_argument('-ip', dest='Adresses', help='targets ip addresss', default=[''], nargs='+')
    arg_parser.add_argument('--verbose', action='store_true',
                            help="Toggle for git diff-like comparasion of config and target configuration")
    args = arg_parser.parse_args()

    for ip in args.Adresses:
        downloader = ConfigDownloader(
            ip, args.username, args.password, ["show ip int brief"])
        with open(f"results/config_{ip}.txt", 'w') as f:
            f.write(downloader.download())

        verbose = True
        config, target = open_files(args.config, f"results/config_{ip}.txt")
        parser = StrictMatchingParser(config, target, verbose)
        parser.parse()
        with open(f"results/result_{ip}.txt", 'w') as f:
            f.write(f"Matches found {parser.score} out of {parser.n_of_tokens}")
