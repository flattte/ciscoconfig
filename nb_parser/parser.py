DEBUG = True

def open_file(path):
    assert type(path) is str, "path must be a string preferably valid xd"
    try:
        f = open(path, 'r')
    except Exception as e:
        exit(f"Exception {e.__class__} occurred while opening {path}.\n")
    return f

class mode:
    active = 0
    passive = 1

class token_wrapper(object):
    def __init__(self, content):
        self.content = content
        self.title = None
        self.body = None 
        if content:
            self.title = content[0]
        if content[1:]:
            self.body = content[1:]

class parser(object):
    def __init__(self, config, target, verbose=False, ignore_ip=True):
        self.config = config
        self.target = target
        self.ignore_ip = ignore_ip
        self.verbose = verbose
        self.target_tokens = []
        self.config_tokens = []

    def tokenize(self, configuration):
        state = mode.passive 
        bad_lines = ['show run', 'Building', 'Current configuration :', 'version']
        ret_tokens = []
        raw_text_token = []
        for line in configuration:
            if any([bad_line in line for bad_line in bad_lines]):
                continue
            if '!' not in line and line:
                if state == mode.passive: state = mode.active
                if line[0] == ' ':
                    raw_text_token.append(line.strip())
                else: 
                    if raw_text_token: ret_tokens.append(token_wrapper(raw_text_token))
                    raw_text_token = [line]
            else:
                if state == mode.active:
                    if raw_text_token: ret_tokens.append(token_wrapper(raw_text_token))
                    raw_text_token = []
                    state = mode.passive
                if state == mode.passive:
                    continue
        return ret_tokens


    def print_token(self, token):
        print(token)
        print("Token title: ", token.title,)
        if token.body:
            print("Token body: ", token.body)
        print()

    def parse(self):
        self.target_tokens = self.tokenize(self.target)
        self.config_tokens = self.tokenize(self.config)
        # for token in self.target_tokens:
        #     print(token.body)
        if DEBUG:
            print([self.print_token(token) for token in self.target_tokens])
            print([self.print_token(token) for token in self.config_tokens])  

if __name__ == "__main__":
    c = open_file("../test/cfg1.txt")
    t = open_file("../test/cfg2.txt")
    config = [line.strip('\n') for line in c.readlines()]
    target = [line.strip('\n') for line in t.readlines()]
    p = parser(config, target)
    p.parse()

