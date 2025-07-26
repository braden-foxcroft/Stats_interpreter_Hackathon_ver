

"""
,
AND OR
== != >= <= < >
to
+ -
* //
not -a
()
[int or str]

grammar
exp1 = exp2 [, exp2]
exp2 = exp3 [and|or exp3]
exp3 = exp4 [==|!=|>=|<=|<|> exp4]
exp4 = exp5 [to exp5]
exp5 = exp6 [+|- exp6]
exp6 = exp7 [*|// exp7]
exp7 = exp8 | (not|-)exp8
exp8 = exp9 | ( exp1 )
exp9 = number | string
string = alpha|_
"""

def parseExp1(feed):
    left = parseExp2(feed)
    while feed.peek == ",":
        oper = feed.pop
        right = parseExp2(feed)
        left = (oper,left,right)
    return left

def parseExp2(feed):
    left = parseExp3(feed)
    while feed.peek in {"and","or"}:
        oper = feed.pop
        right = parseExp3(feed)
        left = (oper,left,right)
    return left

def parseExp3(feed):
    left = parseExp4(feed)
    while feed.peek in {"==","!=",">=","<=","<",">"}:
        oper = feed.pop
        right = parseExp4(feed)
        left = (oper,left,right)
    return left

def parseExp4(feed):
    left = parseExp5(feed)
    while feed.peek == "to":
        oper = feed.pop
        right = parseExp5(feed)
        left = (oper,left,right)
    return left

def parseExp5(feed):
    left = parseExp6(feed)
    while feed.peek in {"+","-"}:
        oper = feed.pop
        right = parseExp6(feed)
        left = (oper,left,right)
    return left

def parseExp6(feed):
    left = parseExp7(feed)
    while feed.peek in {"*","//"}:
        oper = feed.pop
        right = parseExp7(feed)
        left = (oper,left,right)
    return left

def parseExp7(feed):
    if feed.peek == "not":
        oper = feed.pop
        return (oper,parseExp8(feed))
    if feed.peek == "-":
        oper = feed.pop
        return (oper,0,parseExp8(feed))
    return parseExp8(feed)


def parseExp8(feed):
    if feed.peek =="(":
        feed.pop
        res = parseExp1(feed)
        if feed.peek != ")": raise Exception (f"expected close bracket, got {feed.peek}")
        feed.pop
        return res
    return parseExp9(feed)

def parseExp9(feed):
    if isinstance(feed.peek, int) or isinstance(feed.peek,str): return feed.pop

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

    
class Feeder:
    def __init__(self,itr):
        self.__iterable = iter(itr)
        self._nxt()
    def _nxt(self):
        try:
            self.nxt = next(self.__iterable)
        except:
            self.nxt = None
    @property
    def peek(self):
        return self.nxt
    @property
    def pop(self):
        res = self.nxt
        self._nxt()
        return res

def lex(line):
    # "select a from 1,2,3" becomes ["select",... etc.]
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
        elif line.peek=="!":
            line.pop
            if line.peek == "=":
                res.append("!=")
                line.pop
            else:
                res.append("!")
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




################################## weird ass tests
# print(lex(Feeder("Take a feeder of a line, return list of tokens")))
# print(lex(Feeder("(a+b)")))
# print(lex(Feeder("a<=v")))
# print(lex(Feeder("3==5")))
# print(lex(Feeder("33//55")))
# print(lex(Feeder("select a from 1,2,3")))
# print(parseExp1(Feeder(lex(Feeder("a,b")))))
# print(parseExp1(Feeder(lex(Feeder("1 and 2")))))
# print(parseExp1(Feeder(lex(Feeder("11 == 12")))))
# print(parseExp1(Feeder(lex(Feeder("a <=2 ")))))
# print(parseExp1(Feeder(lex(Feeder("2 to a ")))))
# print(parseExp1(Feeder(lex(Feeder("2 > a ")))))
# print(parseExp1(Feeder(lex(Feeder("2+2")))))
# print(parseExp1(Feeder(lex(Feeder("a*a")))))
# print(parseExp1(Feeder(lex(Feeder("      4//4")))))
# print(parseExp1(Feeder(lex(Feeder("a != c")))))
# print(parseExp1(Feeder(lex(Feeder("not a")))))
# print(parseExp1(Feeder(lex(Feeder("-a")))))
print(parseExp1(Feeder(lex(Feeder("(1 and a)"))))) 
