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
    def __init__(self, configuation, verbose=False, ignore_ip=True):
        self.configuation = configuation
        self.ignore_ip = ignore_ip
        self.verbose = verbose
        self.tokens = None
 
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
        ret_ret_tokens = [token for token in ret_tokens if token.body is not None]
        return ret_tokens

    def parse(self):
        self.tokens = self.tokenize(self.configuation)
        if DEBUG:
            pass
            [self.print_token(token) for token in self.tokens]

    def print_token(self, token):
        print("########")
        print("Token title: ", token.title,)
        if token.body is not None:
            print("Token body: ")
            [print("  ", line) for line in token.body]
        print("########")
        print()

class checker(object):
    def __init__(self, config, target): 
        self.config = config
        self.target = target
    
    def check(self): 
        counter_target = 0
        couter_config = 0
        
    @staticmethod
    def similarityMetric(cline, tline):
        intersection_cardinality = len(set.intersection(*[set(cline), set(tline)]))
        union_cardinality = len(set.union(*[set(cline), set(tline)]))
        return intersection_cardinality/float(union_cardinality)

### test
if __name__ == "__main__":
    c = open_file("../test/cfg1.txt")
    t = open_file("../test/cfg2.txt")
    config_file = [line.strip('\n') for line in c.readlines()]
    target_file = [line.strip('\n') for line in t.readlines()]
    config = parser(config_file).parse()
    target = parser(target_file).parse()
    

