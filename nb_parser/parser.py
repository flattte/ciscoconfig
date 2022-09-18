
def open_file(path):
    assert type(path) is str, "path must be a string preferably valid xd"
    try:
        f = open(path, 'r')
    except Exception as e:
        exit(f"Exception {e.__class__} occurred while opening {path}.\n")
    return f


class token(object):
    def __init___(self, content):
        self.content = content
        self.token_is_valid = True
        if not content:
            self.token_is_valid = False    
            return None
        self.title = content[0]
        if not content[1:]: return
        self.body = content[1:]


class mode:
    active = 0
    passive = 1

class parser(object):
    def __init__(self, config, target,
                verbose=False, ignore_ip=True):
        self.config = config
        self.target = target
        self.ignore_ip = ignore_ip
        self.verbose = verbose
        self.target_tokens = []
        self.config_tokens = []

    def tokenize(self, configuration):
        print("configuration")
        print(configuration)
        state = mode.passive 
        bad_lines = ['Current configuration :', 'version']
        ret_tokens = []
        token = []
        for line in configuration:
            if any([bad_line in line for bad_line in bad_lines]):
                continue
            if '!' not in line:
                if state == mode.passive:
                    state = mode.active
                token.append(line)
            else:
                if state == mode.passive:
                    continue
                if state == mode.active:
                    ret_tokens.append(token)
                    token = []
                    state = mode.passive 
    
    def parse(self):
        self.target_tokens = self.tokenize(self.target)
        self.config_tokens = self.tokenize(self.config)
        print(self.target_tokens)
        print(self.config_tokens)
                    
                
                
            
        

if __name__ == "__main__":
    c = open_file("../test/cfg1.txt")
    t = open_file("../test/cfg2.txt")
    config = [line.strip() for line in c.readlines()]
    target = [line.strip() for line in t.readlines()]
    p = parser(config, target)
    p.parse()

