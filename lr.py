import copy
import pprint

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


class lrExpression(object):
    def __init__(self, expr, la, lrpos):
        self.expr = expr
        self.la = la
        self.lrpos = lrpos

    def getLrStart(self):
        return self.expr[self.lrpos]

    def getLrStartLa(self):
        return self.expr[self.lrpos+1:self.lrpos+2]

    def isReduce(self):
        return self.lrpos == len(self.expr)-1

    def __str__(self):
        expr = copy.deepcopy(self.expr)
        expr.insert(self.lrpos, ".")
        return str(expr) + ", " + str(self.la)

    def __repr__(self):
        return self.__str__()

class lrState(object):
    def __init__(self, *args):
        if len(args) == 1:
            self.productions = args[0]
        elif len(args) == 0:
            self.productions = []
        else:
            raise TypeError("__init__() takes 0 or 1 arguments (" + str(len(args)) + " given)")
        
        self.transitions = {}


def fillState(state, lrpos, states, grammar, follows):
    newprods = []
   
    i = 0 
    while i < len(state.productions):
        #print prod[1].getLrStart()

        start = state.productions[i][1].getLrStart()

        if isinstance(start, nonTerminal):
            for gprod in grammar[start.name]:
                state.productions.append([start, lrExpression(gprod, state.productions[i][1].getLrStartLa(), lrpos)])
        
        i += 1

    pp = pprint.PrettyPrinter(indent = 4)
    pp.pprint(state.productions)
        


def getParser(grammar):
    
    follows = {}
    for p in grammar:
        follows[p] = getFollows(nonTerminal(p), grammar)

    states = [ lrState([["START'", lrExpression(grammar["START'"][0], [], 0)]]) ]

    fillState(states[0], 0, states, grammar, follows)


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
    "START'": [[nonTerminal("START"), terminal()]],
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
    
