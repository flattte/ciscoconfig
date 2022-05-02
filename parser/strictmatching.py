from parser.parserutils import tokenizeConfig, printToken, tokenizeTarget
import termcolor


class StrictMatchingParser(object):
    def __init__(self, config, target, verbose):
        self.config = tokenizeConfig(config)
        self.target = tokenizeTarget(target)
        self.matches = []
        self.verbose = verbose
        self.score = 0
    

    def parse(self):
        self.match()
        if self.verbose:
            print("matches :   \n",self.match)


    def match(self):
        m = []
        for c_token in self.config:
            for t_token in self.target:
                if len(c_token) != len(t_token):
                    continue
            
                if all(t_token[i] == c_token[i] for i in range(len(self.target))):
                    match = [t_token, c_token]
                    m.append(match)
        self.matches = m
    
    