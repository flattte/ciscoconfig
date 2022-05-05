#!/usr/bin/python3
from parser.parserutils import ConfigDownloader
from parser.strictmatching import StrictMatchingParser
from parser.parserutils import open_files



if __name__ == "__main__":
    
    downloader = ConfigDownloader("192.168.43.32", "cisco", "cisco", ["show ip int brief"])
    with open("test/remote.txt", 'w') as f:
        f.write(downloader.download())

    verbose = True
    config, target = open_files("test/cfg.txt", "test/remote.txt")
    parser = StrictMatchingParser(config, target, verbose)
    parser.parse()
 
    print(f"Matches found {parser.score} out of {parser.n_of_tokens}")
