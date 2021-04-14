from z3 import *
s = SolverFor("LIA")

#checks if x is an element in l
def oneOf(x, l):
    return Or([ x == p for p in l ])

ops = [ '*', '-', '+', '/' ]

#prints all satisfying arithmetic 2-term combos from lst to get target
def binOp(target, lst):
    a, b = Reals('a b')
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
        if (target not in possibleVals):
            possibleVals.append(target)
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
    a = Int('a')
    achievable = []
    gothru = []
    gothru.extend(given)
    for a in gothru:
        t = Solver()
        t.add(oneIterFor3(a, target, given))
        if t.check() == sat:
            achievable.append(target)
    return achievable

#handles single case if a can be incorated to reach target with rest of lst
def oneIterFor3(a, target, given):
    s = Solver()
    lst = []
    lst.extend(given)
    s.add(Or(findAddValWith(a, target, lst, 2),
             findDivValWith(a, target, lst, 2),
             findSubValWith(a, target, lst, 2),
             findMulValWith(a, target, lst, 2)))
    return s.check() == sat




#prints all satisfying arithmetic 4-term combos from lst to get target
def for4terms(target, given):
    a = Int('a')
    achievable = []
    gothru = []
    gothru.extend(given)
    for a in gothru:
        t = Solver()
        t.add(oneIterFor4(a, target, given))
        if t.check() == sat:
            achievable.append(target)
    return achievable

#handles single case if a can be incorated to reach target with rest of lst
def oneIterFor4(a, target, given):
    s = Solver()
    lst = []
    lst.extend(given)
    s.add(Or(findAddValWith(a, target, lst, 3),
             findDivValWith(a, target, lst, 3),
             findSubValWith(a, target, lst, 3),
             findMulValWith(a, target, lst, 3)))
    return s.check() == sat


#prints all satisfying arithmetic 4-term combos from lst to get target
def for5terms(target, given):
    a = Int('a')
    achievable = []
    gothru = []
    gothru.extend(given)
    for a in gothru:
        t = Solver()
        t.add(oneIterFor5(a, target, given))
        if t.check() == sat:
            achievable.append(target)

#handles single case if a can be incorated to reach target with rest of lst
def oneIterFor5(a, target, given):
    s = Solver()
    lst = []
    lst.extend(given)
    s.add(Or(findAddValWith(a, target, lst, 4),
             findDivValWith(a, target, lst, 4),
             findSubValWith(a, target, lst, 4),
             findMulValWith(a, target, lst, 4)))
    return s.check() == sat   


#returns TRUE if subtracting a helps achieve target with n other terms
def findAddValWith(a, target, lst, n):
    c = target+a
    r = Solver()
    if n == 2:
        r.add(c in binOp(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("        -",a)
    if n == 3:
        r.add(c in for3terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("            -",a)
    if n == 4:
        r.add(c in for4terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("                -",a)
    return r.check() == sat

#returns TRUE if adding a helps achieve target with n other terms
def findSubValWith(a, target, lst, n):
    c = target-a
    r = Solver()
    if n == 2:
        r.add(c in binOp(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("        +",a)
    if n == 3:
        r.add(c in for3terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("            +",a)
    if n == 4:
        r.add(c in for4terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("                +",a)
    return r.check() == sat

#returns TRUE if dividing a helps achieve target with n other terms
def findMulValWith(a, target, lst, n):
    c = target*a
    r = Solver()
    if n == 2:
        r.add(c in binOp(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("        /",a)
    if n == 3:
        r.add(c in for3terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("            /",a)
    if n == 4:
        r.add(c in for4terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("                /",a)
    return r.check() == sat

#returns TRUE if multiplying a helps achieve target with n other terms   
def findDivValWith(a, target, lst, n):
    c = float(target)/a
    r = Solver()
    if n == 2:
        r.add(c in binOp(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("        *",a)
    if n == 3:
        r.add(c in for3terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("            *",a)
    if n == 4:
        r.add(c in for4terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("                *",a)
    return r.check() == sat
