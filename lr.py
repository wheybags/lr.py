def getFollows(sym, grammar):
    follows = []

    for p in grammar:
        for e in grammar[p]:
            for i in range(len(e)):
                if e[i] == sym:
                    if i == len(e)-1:
                        follows += getFollows(nonTerminal(p), grammar)
                    else:
                        follows.append(e[i+1])
    
    return follows



def getParser(grammar):
    
    follows = {"START": [terminal()]}
    for p in grammar:
        if p != "START":
            follows[p] = getFollows(nonTerminal(p), grammar)

    print follows


class token(object):
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.name == other.name
    def __str__(self):
        return type(self).__name__ + "(" + self.name + ")"
    
    def __repr__(self):
        return self.__str__()

class terminal(token):
    
    def __init__(self, *args, **kwargs):
        
        if len(args) == 0:
            self.end = True
            args = [""]

        super(terminal, self).__init__(*args, **kwargs)

class nonTerminal(token):
    pass

grammar = {
    "START": [
        [nonTerminal("A"), terminal("a")], 
        [terminal("b"), nonTerminal("A"), terminal("c")],
        [nonTerminal("B"), terminal("c")],
        [terminal("b"), nonTerminal("B"), terminal("a")]
    ],
    "A": [[terminal("d")]],
    "B": [[terminal("d")]]
}

getParser(grammar)
    
