class token(object):
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.name == other.name
    def __str__(self):
        return type(self).__name__ + ("(\"" + self.name + "\")" if self.name != "" else "()")
    
    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.__repr__().__hash__()

class terminal(token):
    
    def __init__(self, *args, **kwargs):
        
        if len(args) == 0:
            self.end = True
            args = [""]

        super(terminal, self).__init__(*args, **kwargs)

class nonTerminal(token):
    pass
