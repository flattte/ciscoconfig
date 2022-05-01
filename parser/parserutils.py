import os
import termcolor

def tokenizeConfig(config) -> list():
    token, tokens = [], []
    for line in config.read().splitlines():
        if '!' in line:
            if token: tokens.append(token)
            token = []
        else:
            token.append(line.strip("\t ").strip(" "))

    return tokens


def yieldToken(token):
    yield token[1][1]
    for t in token[1][0]:
        yield t
    
    
def printToken(token, color="white") -> None:
    if os.name == "nt":
        os.system("color")
    g = yieldToken(token)
    print("Query:")
    print(termcolor.colored(f"    {next(g)}", color))
    print("Body:")
    [print(termcolor.colored(f"    {next(g)}", color)) for _ in range(len(token[1][0]))]
    print()