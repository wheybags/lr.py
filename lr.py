import copy

from token import *

class lrExpression(object):
    def __init__(self, expr, la, lrpos):
        self.expr = expr
        self.la = la
        self.lrpos = lrpos

    def getLrStart(self):
        if self.lrpos >= len(self.expr):
            return 
        return self.expr[self.lrpos]

    def getLrStartLa(self):
        return self.expr[self.lrpos+1:self.lrpos+2]

    def isReduce(self):
        return self.lrpos == len(self.expr)

    def __str__(self):
        expr = copy.deepcopy(self.expr)
        expr.insert(self.lrpos, ".")
        return str(expr) + " | " + str(self.la)

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

    def strProductions(self):
        s = ""

        for p in self.productions:
            s += str(p[0]) + " --> " + str(p[1]) + "\n"

        return s


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


def fillState(stateNum, lrpos, states, grammar, follows):
    newStates = set()
    
    state = states[stateNum]
    
    i = 0 
    while i < len(state.productions):
        start = state.productions[i][1].getLrStart()
        if(start):
            if isinstance(start, nonTerminal):
                for gprod in grammar[start.name]:
                    state.productions.append([start, lrExpression(gprod, state.productions[i][1].getLrStartLa(), 0)])
            
            if not state.productions[i][1].isReduce():
                if not start in state.transitions:
                    states.append(lrState())
                    state.transitions[start] = len(states)-1
                    newStates.add(state.transitions[start])
                
                newprod = copy.deepcopy(state.productions[i])
                newprod[1].lrpos += 1
                states[state.transitions[start]].productions.append(newprod)
                
        i += 1

    for s in newStates:
        fillState(s, lrpos, states, grammar, follows)

def genFunc(stateNum, states):
    state = states[stateNum]
    
    func =  "    def func" + str(stateNum) + "(states, stack, input):\n"
    func += "        state = states[" + str(stateNum) + "]\n"
    func += "        tok = nextTok(input)\n"
    func += "        if tok in state:\n"
    func += "            advance(input)\n"
    func += "            stack.append(tok)\n"
    func += "            stack.append(state[tok])\n"
    func += "            return state[tok]\n"

    for prodnum in range(len(state.productions)):
        prod = state.productions[prodnum]
        if prod[1].isReduce():
            func += "        if lookahead(input) == "+ str(prod[1].la) + " and"
            for i in range(len(prod[1].expr)):
                func += " " + str(prod[1].expr[i]) + " == stack[" + str(2*i) + " + abs(len(stack)-" + str(len(prod[1].expr)*2) + ")] and"
            
            func = func[:-4]
            func += ":\n"
            func += "            del stack[-" + str(2*len(prod[1].expr)) + ":]\n"
            func += "            input.insert(0, " + str(prod[0]) + ")\n"
            func += "            # ----- action here\n"
            func += "            return stack[-1]\n"
            

    return func

def getParser(grammar):
    
    follows = {}
    for p in grammar:
        follows[p] = getFollows(nonTerminal(p), grammar)

    states = [ lrState([[nonTerminal("START'"), lrExpression(grammar["START'"][0], [], 0)]]) ]

    fillState(0, 0, states, grammar, follows)
    
    code =  "from token import terminal, nonTerminal\n" 
   
    code += "def parse(input):\n"
    
    code += "    def nextTok(input):\n"
    code += "        if len(input) == 0:\n"
    code += "            return None\n"
    code += "        return input[0]\n"
    code += "    def advance(input):\n"
    code += "        retval = input[0]\n"
    code += "        del input[0]\n"
    code += "        return retval\n"
    code += "    def lookahead(input):\n"
    code += "        return input[0:1]\n"

    for i in range(len(states)):
        code += genFunc(i, states)

    code += "    stack = [0]\n"
    code += "    states = ["
    for s in states:
        code += str(s.transitions) + ", "

    code = code[:-2]
    code += "]\n"

    code += "    funcs = ["
    for i in range(len(states)):
        code += "func" + str(i) + ", "
    code = code[:-2]
    code += "]\n"

    code += "    current = 0\n"
    code += "    while not (stack == [0] and input == [nonTerminal(\"START'\")]):\n"
    code += "        print current\n"
    code += "        print stack\n"
    code += "        print input\n"
    code += "        print\n"
    code += "        current = funcs[current](states, stack, input)\n"

    exec code

    return parse


def main():
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

    parse = getParser(grammar)
    
    parse([terminal("d"), terminal("c"), terminal()])

if __name__ == "__main__":
    main()
