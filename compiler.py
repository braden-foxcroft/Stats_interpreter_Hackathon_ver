

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

parseExp = parseExp1

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
    '#': 'comment',
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
    while line.peek == "\t": res.append(line.pop)
    if line.peek == "#": # Comment
        while line.peek != None: line.pop
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
            if len(string): res.append(string)
            continue
        continue
    return res

def getBlock(lines):
    res = []
    while lines.peek != None and lines.peek.peek == "\t":
        lines.peek.pop
        res.append(lines.pop)
    return res


def parseLine(line,lines):
    if line.peek == None: return None
    if line.peek == "pass": return ("pass",)
    if line.peek == "fail": return ("fail",)
    if line.peek == "done": return ("done",)
    if line.peek == "good": return ("good",)
    if line.peek == "bad": return ("bad",)
    if line.peek == "debug": return ("debug",)
    if line.peek == "select":
        line.pop
        var = line.pop
        if line.peek != "from": raise Exception(f"Expected from, got: {line.peek}")
        line.pop
        expr = parseExp(line)
        if line.peek == "where":
            line.pop
            expr2 = parseExp(line)
        else:
            expr2 = 1
        return ("select",var,expr,expr2)
    if line.peek == "set":
        line.pop
        var = line.pop
        if line.peek != "=": raise Exception(f"Expected '=', got: {line.peek}")
        line.pop
        expr = parseExp(line)
        return ("set",var,expr)
    if line.peek == "bychance":
        line.pop
        expr = parseExp(line)
        return ("bychance",expr)
    if line.peek == "discard":
        line.pop
        return ("discard",line.pop)
    if line.peek == "if":
        line.pop
        expr = parseExp(line)
        block = parseBlock(Feeder(getBlock(lines)))
        if lines.peek != None and lines.peek.peek == "else":
            lines.pop
            block2 = parseBlock(Feeder(getBlock(lines)))
            return ("if",expr,block,block2)
        return ("if",expr,block,[])
    if line.peek == "for":
        line.pop
        var = line.pop
        if line.peek not in {"from","in"}: raise Exception(f"Expected 'from' or 'in' in 'for' loop, got {line.peek}")
        line.pop
        expr = parseExp(line)
        block = parseBlock(Feeder(getBlock(lines)))
        return ("for",var,expr,block)
    if line.peek == "print":
        line.pop
        expr = parseExp(line)
        return ("print",expr)
    raise Exception(f"Unknown command: {list(iter(lambda : line.pop,None))}")
    
    

def parseBlock(lines):
    res = []
    while lines.peek != None:
        line = lines.pop
        if line.peek == None:
            line.pop
            continue
        res.append(parseLine(line,lines))
    return res
    


def compile(file):
    lines = file.readlines()
    lines = Feeder([Feeder(lex(Feeder(line))) for line in lines])
    tree = parseBlock(lines)
    return tree # Tree




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
