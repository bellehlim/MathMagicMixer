from z3 import *
s = SolverFor("LIA")

#checks if x is an element in l
def oneOf(x, l):
    return Or([ x == p for p in l ])

ops = [ '*', '-', '+', '/' ]

#prints all satisfying arithmetic 2-term combos from lst to get target
def binOp(target, lst):
    a, b = Ints('a b')
    o = String('o')
    possibleVals = []
    t = Solver()
    t.add(Or (And(o == '*', a * b == target),
              And(o == '+', a + b == target),
              And(o == '-', a - b == target),
              And(o == '/', a / b == target)),
                        oneOf(a, lst),
                        oneOf(b, lst),
                        oneOf(o, ops),
                        Distinct(a, b))
    while t.check() == sat:
        first = t.model()[a].as_long()
        second = t.model()[b].as_long()
        op = t.model()[o]
        print (first, op, second)
        t.add(Not(And(a == t.model()[a],
                      o == t.model()[o],
                      b == t.model()[b])))
    return possibleVals

#returns list with a removed
def removeFrom(a, lst):
    if a in lst:
        lst.remove(a)
        return lst
    else:
        return lst
    
#prints all satisfying arithmetic 3-term combos from lst to get target
def for3terms(target, given):
    t = Solver()
    a = Int('a')
    gothru = []
    gothru.extend(given)
    for a in gothru:
        t.add(oneIterFor3(a, target, given))
    
#handles single case if a can be incorated to reach target with rest of lst
def oneIterFor3(a, target, given):
    o = String('o')
    s = Solver()
    lst = []
    lst.extend(given)
    print("\n")
    s.add(Or(findAddVal(a, target, lst),
             findDivVal(a, target, lst),
             findSubVal(a, target, lst),
             findMulVal(a, target, lst)))
    return s.check() == sat

    
#returns TRUE if subtracting a (3rd term) helps achieve b in lst
def findAddVal(a, b, lst):
    c = b+a
    r = Solver()
    r.add(oneOf(a, lst), c in binOp(c, removeFrom(a, lst)))
    print("        -", a)
    return r.check() == sat

#returns TRUE if adding a (3rd term) helps achieve b in lst
def findSubVal(a, b, lst):
    c = b-a
    r = Solver()
    r.add(oneOf(a, lst), c in binOp(c, removeFrom(a, lst)))
    print("        +",a)
    return r.check() == sat

#returns TRUE if dividing a (3rd term) helps achieve b in lst
def findMulVal(a, b, lst):
    c = b*a
    r = Solver()
    r.add(oneOf(a, lst), c in binOp(c, removeFrom(a, lst)))
    print("        /", a)
    return r.check() == sat

#returns TRUE if multiplying a (3rd term) helps achieve b in lst        
def findDivVal(a, b, lst):
    c = b/a
    r = Solver()
    r.add(oneOf(a, lst), c in binOp(c, removeFrom(a, lst)))
    print("        *",a)
    return r.check() == sat


#NOTES:
#for3terms(34, [6, 5, 2, 4, 3]) -- case where decimals need to be handled
