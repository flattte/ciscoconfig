from parser.parserutils import tokenizeConfig, printToken, tokenizeTarget



class StrictMatchingParser(object):
    def __init__(self, config, target, verbose = False, ignore_ip = True):
        self.config = tokenizeConfig(config)
        self.target = tokenizeTarget(target)
        self.matches = []
        self.score = 0
        self.n_of_tokens = len(self.target)
        self.ignore_ip = ignore_ip
        self.verbose = verbose



    def parse(self):
        self.match()
        if self.verbose:
            [print(m[0],"\n", m[1], "\n\n") for m in self.matches]
            print(f"Matched {self.score} out of {self.n_of_tokens}")


    
    def verifyToken(self, t_token, c_token) -> bool:
        if self.ignore_ip:
            for t, c in zip(t_token.split(), c_token.split()):
                if t == c or t=="###":
                    continue    
                if t != c:
                    return False    
            return True
        else:
            return t_token == c_token



    def match(self):
        m = []
        for c_token in self.config:
            for t_token in self.target:
                if len(c_token) != len(t_token):
                    continue
                
                if all(self.verifyToken(t_token[i], c_token[i]) for i in range(len(c_token))):
                    match = [t_token, c_token]
                    m.append(match)
        self.matches = m
        self.score = len(m)
    
