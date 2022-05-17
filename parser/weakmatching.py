import termcolor
from parser.parserutils import printToken, tokenizeConfig

# parsing cisco config to get exact, similiar and completely wrong answers


class WeakMatchingParser(object):
    def __init__(self, config, target, verbose):
        self.config = tokenizeConfig(config)
        self.target = [line for line in target.read().splitlines()]
        self.verbose = verbose
        self.score = 0
        self.n_of_tokens = 0

    def parse(self) -> None:
        matches = self.matchTokens()
        best = self.getBest(matches)
        for t in best:
            self.oracle(t, self.verbose)

    def matchTokens(self) -> list():
        matches = []
        for t_token in self.target:
            match = {}
            for c_token in self.config:
                match[max([self.similarityMetric(cline, t_token)
                          for cline in c_token])] = [c_token, t_token]
            matches.append(match)
        self.n_of_tokens = len(matches)
        return matches

    def getBest(self, matches) -> list():
        mx = []
        for match in matches:
            mx.append([(key, value) for key, value in match.items()])
        # data frame:
        #   result[0]     - metric score
        #   results[1][0] - body of a token
        #   results[1][1] - query
        return [max(zip(m))[0] for m in mx]

    def oracle(self, token, verbose) -> None:
        if token[1][1].lower() in [t.lower() for t in token[1][0]]:
            if verbose:
                printToken(token, color="green")
            self.score += 1
        elif token[0] > 0.55:
            if verbose:
                printToken(token, color="yellow")
        else:
            if verbose:
                printToken(token, color="red")

    # might use another one if this proves not accurate enough
    def similarityMetric(self, cline, tline) -> float:
        intersection_cardinality = len(
            set.intersection(*[set(cline), set(tline)]))
        union_cardinality = len(set.union(*[set(cline), set(tline)]))

        return intersection_cardinality/float(union_cardinality)
