



def getExample(st):
    if st == "0": return [("pass",)]
    if st == "1": return [("fail",)]
    if st == "2": return [("done",)]
    if st == "3": return [("good",),("good",)]
    if st == "4": return [("bad",),("bad",)]
    if st == "5": return [("set","q",("+",1,("*",2,3)))]
    if st == "6": return [("set","a",("//",5,("-",3,1)))]
    if st == "7": return [("set","a",("to",1,4))]
    if st == "8": return [("set","a",(",",("to",1,4),(",",5,6)))]
    if st == "9": return [("set","a",("and",0,"a"))]
    if st == "10": return [("set","a",("or",1,"a"))]
    if st == "11": return [("set","a",("and",1,"a"))]
    if st == "12": return [("set","a",("or",0,"a"))]
    if st == "13": return [("select","a",(",",1,(",",2,3)))] # TODO
    raise Exception("Example not found")
