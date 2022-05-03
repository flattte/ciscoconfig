from parser.parserutils import tokenizeConfig, printToken, tokenizeTarget
import termcolor


class StrictMatchingParser(object):
    def __init__(self, config, target, verbose):
        self.config = tokenizeConfig(config)
        self.target = tokenizeTarget(target)
        self.matches = []
        self.verbose = verbose
        self.score = 0
        self.n_of_tokens = len(self.target)
    

    def parse(self):
        self.match()
        if self.verbose:
            [print(m[0],"\n", m[1], "\n\n") for m in self.matches]
            print(f"Matched {self.score} out of {self.n_of_tokens}")

    def match(self):
        m = []
        for c_token in self.config:
            for t_token in self.target:
                if len(c_token) != len(t_token):
                    continue
            
                if all(t_token[i] == c_token[i] for i in range(len(c_token))):
                    match = [t_token, c_token]
                    m.append(match)
        self.matches = m
        self.score = len(m)
    