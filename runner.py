

import compiler
import argparse
from fractions import Fraction as Frac

parser = argparse.ArgumentParser(description="An interpreter which solves stats problems")
parser.add_argument("filename",help="the file to run")
parser.add_argument("-p",help="Give a percentage result",action="store_true")
parser.add_argument("-D",help="print debug info",action="store_true")
parser.add_argument("-e",help="Use an example AST for testing",action="store",default=None)
args = parser.parse_args()

debug = args.D
if debug: print(args)

if args.filename != "":
    with open(args.filename) as file:
        ast = compiler.compile(file)
elif args.e:
    import exampleAsts
    ast = exampleAsts.getExample(args.e)
else:
    ast = []

class Context:
    """Contains:
    - dict of sorted((var,val)) -> frac odds
    - sums: frac pass, frac fail, frac done, frac good, frac bad"""
    def __init__(this,contexts=None):
        if isinstance(contexts,Context):
            c = contexts
            this._pass = c._pass
            this._fail = c._fail
            this._done = c._done
            this._good = c._good
            this._bad = c._bad
            this._contexts = dict()
            return
        if contexts == None: this._contexts = dict()
        else: this._contexts = dict(contexts)
        this._pass = Frac(0)
        this._fail = Frac(0)
        this._done = Frac(0)
        this._good = Frac(0)
        this._bad = Frac(0)
    
    def dopass(this,res):
        this._pass += res
    def dofail(this,res):
        this._fail += res
    def dodone(this,res):
        this._done += res
    def dogood(this,res):
        this._good += res
    def dobad(this,res):
        this._bad += res
    def addContext(this,new,chance):
        if isinstance(new,dict):
            new = tuple(sorted(new.items()))
        if new in this.contexts:
            this._contexts[new] += chance
        else:
            this._contexts[new] = chance
    @property
    def contexts(this):
        return iter(this._contexts.items())
    def __str__(this):
        return str({"cont":this._contexts,"pass":this._pass,"fail":this._fail,"done":this._done,"good":this._good,"bad":this._bad})
    def __repr__(this):
        return str(this)
    
    def __add__(this,c):
        if not isinstance(c,Context): raise Exception(f"add took type: {type(c)}")
        new = Context(this)
        new._pass += c._pass
        new._fail += c._fail
        new._done += c._done
        new._good += c._good
        new._bad += c._bad
        for con,fr in this.contexts:
            new.addContext(con,fr)
        for con,fr in c.contexts:
            new.addContext(con,fr)
        return new
        

def con2dict(con):
    """Takes a context as a tuple of tuples, returns a dict(varname->val)"""
    res = dict()
    for a,b in con:
        res[a] = b
    return res


"""
>= <= == != > <
not
and or
+ - * //
, to
ints
varnames
"""
def Eval(expr,con):
    """Takes an expr, dict(varname->val)"""
    if isinstance(expr,int): return expr
    if isinstance(expr,str):
        if expr in con: return con[expr]
        raise Exception(f"Var not found: \"{expr}\"")
    if expr == "not":
        r1 = Eval(expr[1],con)
        if not isinstance(r1,int): raise Exception(f"Bad type: {expr}")
        return int(not r1)
    if expr[0] == "and":
        r1 = Eval(expr[1],con)
        if not isinstance(r1,int): raise Exception(f"Bad type (left): {expr}")
        if not r1: return r1
        r2 = Eval(expr[2],con)
        if not isinstance(r2,int): raise Exception(f"Bad type (right): {expr}")
        return r2
    if expr[0] == "or":
        r1 = Eval(expr[1],con)
        if not isinstance(r1,int): raise Exception(f"Bad type (left): {expr}")
        if r1: return r1
        r2 = Eval(expr[2],con)
        if not isinstance(r2,int): raise Exception(f"Bad type (right): {expr}")
        return r2
    if expr[0] == ",":
        r1 = Eval(expr[1],con)
        r2 = Eval(expr[2],con)
        if isinstance(r1,int): r1 = (r1,)
        if isinstance(r2,int): r2 = (r2,)
        return r1 + r2
    if expr[0] in [">=","<=","==","<",">","!=","+","*","//","-","to"]:
        r1 = Eval(expr[1],con)
        r2 = Eval(expr[2],con)
        if not isinstance(r1,int): raise Exception(f"Bad type (left): {expr}")
        if not isinstance(r2,int): raise Exception(f"Bad type (right): {expr}")
        if expr[0] == ">=": return r1 >= r2
        if expr[0] == "<=": return r1 <= r2
        if expr[0] == "==": return r1 == r2
        if expr[0] == "<": return r1 < r2
        if expr[0] == ">": return r1 > r2
        if expr[0] == "!=": return r1 != r2
        if expr[0] == "+": return r1 + r2
        if expr[0] == "*": return r1 * r2
        if expr[0] == "//": return r1 // r2
        if expr[0] == "-": return r1 - r2
        if expr[0] == "to": return tuple(range(r1,r2+1))
        raise Exception(f"Unknown operation: {expr[0]}")
    raise Exception(f"Unknown operation: {expr[0]}")



# Carry out a block's worth of action.
def doBlock(block,old):
    """Takes block, context.
    Returns context"""
    for line in block:
        new = Context(old)
        if line[0] == "select":
            var = line[1]
            expr = line[2]
            expr2 = line[3]
            for con,fr in old.contexts:
                cond = con2dict(con)
                res = Eval(expr,cond)
                news = []
                if not isinstance(res,tuple): raise Exception("Select took non-list")
                for r in res:
                    d = dict(cond)
                    d[var] = r
                    news.append(d)
                new2 = []
                for n in news:
                    res = Eval(expr2,n)
                    if not isinstance(res,int): raise Exception("select condition was non-int")
                    if res: new2.append(n)
                l = len(new2)
                for n in new2:
                    new.addContext(n,fr / l)
        elif line[0] == "set":
            var = line[1]
            expr = line[2]
            for con,fr in old.contexts:
                res = Eval(expr,con)
                cond = con2dict(con)
                cond[var] = res
                new.addContext(cond,fr)
        elif line[0] == "if":
            # Split
            yes = Context(old)
            no = Context(old)
            for con,fr in old.contexts:
                cond = con2dict()
                res = Eval(line[1],cond)
                if not isinstance(res,int): raise Exception(f"'if' didn't return int: {line[1]}")
                if res:
                    yes.addContext(cond,fr)
                else:
                    no.addContext(cond,fr)
            res1 = doBlock(line[2],yes)
            res2 = doBlock(line[3],no)
            new = res1 + res2
        elif line[0] == "discard":
            for con,fr in old.contexts:
                cond = con2dict(con)
                if line[1] in cond: del cond[line[1]]
                new.addContext(cond,fr)
        elif line[0] == "for":
            options = dict()
            var = line[1]
            for con,fr in old.contexts:
                cond = con2dict(con)
                res = Eval(line[2],cond)
                if not isinstance(res,tuple): raise Exception(f"'for' didn't take tuple: {line[2]}")
                if res not in options:
                    options[res] = Context(old)
                options[res].addContext(cond,fr)
            res = Context()
            for tpl in options:
                old2 = options[tpl]
                for i in tpl:
                    # Update vars
                    new = Context(old2)
                    for con,fr in old2.contexts:
                        cond = con2dict(con)
                        cond[var] = i
                        new.addContext(cond,fr)
                    new = doBlock(line[3],new)
                res = res + new
            new = res
        elif line[0] == "print":
            for con,fr in old.contexts:
                cond = con2dict(con)
                print(Eval(line[1],cond))
            new = old
        elif line[0] == "pass":
            for _,fr in old.contexts:
                new.dopass(fr)
        elif line[0] == "fail":
            for _,fr in old.contexts:
                new.dofail(fr)
        elif line[0] == "done":
            for _,fr in old.contexts:
                new.dodone(fr)
        elif line[0] == "good":
            for con,fr in old.contexts:
                new.dogood(fr)
                new.addContext(con,fr)
        elif line[0] == "bad":
            for con,fr in old.contexts:
                new.dobad(fr)
                new.addContext(con,fr)
        else:
            raise Exception(f"Unknown command: {line[0]}")
        old = new
    return old

# Carry out the entire program.
def doprog(block):
    """Takes a program. Returns a context"""
    old = Context({():Frac(1,1)})
    return doBlock(block,old)
    

print(doprog(ast))




