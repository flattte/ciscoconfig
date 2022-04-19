import functools
import os
import termcolor
import main

def tokenizeConfig(config):
    token, tokens = [], []
    for line in config.read().splitlines():
        if '!' in line:
            if token: tokens.append(token)
            token = []
        else:
            token.append(line.strip("\t ").strip(" "))

    return tokens

#might use another one if this proves not accurate enough
def similarityMetric(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    
    return intersection_cardinality/float(union_cardinality)


def matchTokens(config_tokens, target_tokens):
    matches = [] # for each token in target_tokens here will be matches dictionary under respective index
    for t_token in target_tokens:
        match = {}
        for c_token in config_tokens:
            match[max([similarityMetric(cline, t_token) for cline in c_token])] = [c_token, t_token]
        matches.append(match)   
    
    return matches


def getBest(matches):
    mx =[]
    for match in matches:
        mx.append([(key, value) for key, value in match.items()])
    
    return [max(zip(m))[0] for m in mx]


def yieldToken(token):
    yield token[1][1]
    for t in token[1][0]:
        yield t


def printToken(token, color="white"):
    os.system("color")
    g = yieldToken(token)
    print("Query:")
    print(termcolor.colored(f"    {next(g)}", color))
    print("Body:")
    [print(termcolor.colored(f"    {next(g)}", color)) for _ in range(len(token[1][0]))]
    print()


def oracle(token, verbose, count):
    if token[1][1].lower() in [t.lower() for t in token[1][0]]:
        if verbose: printToken(token, color="green")
        count[0] += 1
    elif token[0] > 0.55:
        if verbose: printToken(token, color="yellow")
    else:
        if verbose: printToken(token, color="red")