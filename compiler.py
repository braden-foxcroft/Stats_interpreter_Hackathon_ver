
tokens = {
    '(': 'LEFT_PAREN',
    ')': 'LEFT_PAREN',
    '+': 'BINARY_ADD',
    '-': 'BINARY_SUB',
    # '//': 'BINARY_DIVIDE',
    '*': 'BINARY_MUL',
    '-': 'UNARY_NEGATIVE',
    ',': 'BINARY_APPEND',
    # '<': 'LESS_THAN',
    # '>': 'GREATER_THAN',
    # '=': 'EQUALS',
}
    # 'not': 'UNARY_NOT',
    # 'or': 'BINARY_OR',
    # 'and': 'BINARY_AND',
    # 'to': 'BINARY_TO_RANGE',
    # 'let': 'VAR_DECLARE',
    # 'if': 'IF_COND',
    # 'else': 'ELSE_COND',
    # 'good': 'BOOL_TRUE',
    # 'bad': 'BOOK_FALSE',
    # 'for': 'FOR_ITER',
    # 'in': 'BINARY_ITERABLE',
    # 'done': 'TERMINATE',
    # 'good': 'SUCCESS',
    # 'bad': 'FAIL',
    # 'pass': 'TERM_SUCCESS',
    # 'fail': 'TERM_FAIL',
    # 'from': '',
    # ==
    # <=
    # >=
    # !=

class Parser:
    pass
    
class Feeder:
    def __init__(self,itr):
        # init with iterable
        self.__iterable = iter(itr)
        self._nxt()

    def _nxt(self):
        try:
            self.nxt = next(self.__iterable)
        except:
            self.nxt = None

    @property
    def peek(self):
        # peek to check next without popping
        return self.nxt

    @property
    def pop(self):
        # pop to  check next and remove
        res = self.nxt
        self._nxt()
        return res

def lex(line):
    # """Take a feeder of a line, return list of tokens"""
    # "select a from 1,2,3"
    # ["select",]
    # '(': 'LEFT_PAREN',
    # ')': 'LEFT_PAREN',
    # '+': 'BINARY_ADD',
    # '-': 'BINARY_SUB',
    # '//': 'BINARY_DIVIDE',
    # '*': 'BINARY_MUL',
    # '-': 'UNARY_NEGATIVE',
    # ',': 'BINARY_APPEND',
    res = []
    string = ""
    while line.peek != None:
        while line.peek != None and line.peek.isspace(): line.pop
        if line.peek in tokens:
            res.append(line.pop)
            continue
        elif line.peek=="/":
            if line.pop == line.peek:
                res.append("//")
                line.pop
                continue
        elif line.peek=="=":
            line.pop
            if line.peek == "=":
                res.append("==")
                line.pop
            else:
                res.append("=")
            continue
        elif line.peek=="<":
            line.pop
            if line.peek == "=":
                res.append("<=")
                line.pop
            else:
                res.append("<")
            continue
        elif line.peek==">":
            line.pop
            if line.peek == "=":
                res.append(">=")
                line.pop
            else:
                res.append(">")
            continue
        else:
            string = ""
            # handle integers
            while line.peek!=None and line.peek.isdigit():
                string+=line.pop
            if len(string)!=0: 
                res.append(int(string))
                continue
            while line.peek!=None and line.peek in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_":
                string += line.pop
            res.append(string)
            continue
        continue
    return res

 
def compile(file):
    with open(file) as f:
        lines = f.readlines()
        lines = Feeder([Feeder(line) for line in lines])
        parsedTokens=[]
        line = lines.peek()
        parsedTokens.append(lex(line))#returns tokens 
        tree = Parser(tokens)
    return tree or None # Tree


# print(lex(Feeder("Take a feeder of a line, return list of tokens")))
# print(lex(Feeder("(a+b)")))
# print(lex(Feeder("a<=v")))
# print(lex(Feeder("3==5")))
# print(lex(Feeder("select a from 1,2,3")))