from z3 import *
s = SolverFor("LIA")

#checks if x is an element in l
def oneOf(x, l):
    return Or([ x == p for p in l ])

ops = [ '*', '-', '+', '/' ]

#prints all satisfying arithmetic 2-term combos from lst to get a target value
def binOp(target, lst):
    a, b = Reals('a b')
    o = String('o')
    possibleVals = []
    t = Solver()
    #track operation and check result against target
    t.add(Or (And(o == '*', a * b == target),
              And(o == '+', a + b == target),
              And(o == '-', a - b == target),
              And(o == '/', a / b == target)),
                        #vals must come from given list
                        oneOf(a, lst),
                        oneOf(b, lst),
                        oneOf(o, ops),
                        #TODO: allow same a, b if repeats in lst
                        Distinct(a, b))
    while t.check() == sat:
        #need to append target to possible results at least once
        if (target not in possibleVals):
            possibleVals.append(target)
        #extract satisfying values from model
        first = t.model()[a].as_long()
        second = t.model()[b].as_long()
        op = t.model()[o]
        print (first, op, second)
        #record as having printed so future models to not repeat same values
        t.add(Not(Or(And(a == t.model()[a],
                         o == t.model()[o],
                         b == t.model()[b])),
                      #TODO: don't allow repeats such as (3*4) and (4*3)
                    (And(a == t.model()[b],
                         o == t.model()[o],
                         b == t.model()[a]))))
    #necessary for higher iterations
    return possibleVals

#returns list with _a_ removed if present
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
    #attempt to incorporate each term into calculating the target
    for a in gothru:
        t = Solver()
        t.add(oneIterFor3(a, target, given))
        if t.check() == sat:
            achievable.append(target)
    #necessary for higher iterations
    return achievable

#handles single case if _a_ can be incorperated to reach target with rest of lst
def oneIterFor3(a, target, given):
    s = Solver()
    lst = []
    lst.extend(given)
    #find if operating on _a_ helps achieve the target with 2 of the remaining lst values
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
    #attempt to incorporate each term into calculating the target
    for a in gothru:
        t = Solver()
        t.add(oneIterFor4(a, target, given))
        if t.check() == sat:
            achievable.append(target)
    #necessary for higher iterations        
    return achievable

#handles single case if a can be incorperated to reach target with rest of lst
def oneIterFor4(a, target, given):
    s = Solver()
    lst = []
    lst.extend(given)
    #find if operating on _a_ helps achieve the target with 3 of the remaining lst values
    s.add(Or(findAddValWith(a, target, lst, 3),
             findDivValWith(a, target, lst, 3),
             findSubValWith(a, target, lst, 3),
             findMulValWith(a, target, lst, 3)))
    return s.check() == sat


#prints all satisfying arithmetic 4-term combos from lst to get target
def for5terms(target, given):
    #checks inputs are valid
    valid_inputs = [1, 2, 3, 4, 5, 6]
    valid_range = range(6, 37)
    for n in given:
        if n not in valid_inputs or target not in valid_range:
            print("not a valid input!")
            return;
    a = Int('a')
    achievable = []
    gothru = []
    gothru.extend(given)
    #attempt to incorporate each term into calculating the target
    for a in gothru:
        t = Solver()
        t.add(oneIterFor5(a, target, given))
        if t.check() == sat:
            achievable.append(target)

#handles single case if a can be incorperated to reach target with rest of lst
def oneIterFor5(a, target, given):
    s = Solver()
    lst = []
    lst.extend(given)
    #find if operating on _a_ helps achieve the target with 4 of the remaining lst values
    s.add(Or(findAddValWith(a, target, lst, 4),
             findDivValWith(a, target, lst, 4),
             findSubValWith(a, target, lst, 4),
             findMulValWith(a, target, lst, 4)))
    return s.check() == sat   


#returns TRUE if subtracting a helps achieve target with n other terms
def findAddValWith(a, target, lst, n):
    c = target+a
    r = Solver()
    #iterate for 2 remaining terms
    if n == 2:
        r.add(c in binOp(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("        -",a)
    #iterate for 3 remaining terms
    if n == 3:
        r.add(c in for3terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("            -",a)
    #iterate for 4 remaining terms        
    if n == 4:
        r.add(c in for4terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("                -",a)
    return r.check() == sat

#returns TRUE if adding a helps achieve target with n other terms
def findSubValWith(a, target, lst, n):
    c = target-a
    r = Solver()
    #iterate for 2 remaining terms   
    if n == 2:
        r.add(c in binOp(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("        +",a)
    #iterate for 3 remaining terms   
    if n == 3:
        r.add(c in for3terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("            +",a)
    #iterate for 4 remaining terms   
    if n == 4:
        r.add(c in for4terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("                +",a)
    return r.check() == sat

#returns TRUE if dividing a helps achieve target with n other terms
def findMulValWith(a, target, lst, n):
    c = target*a
    r = Solver()
    #iterate for 2 remaining terms 
    if n == 2:
        r.add(c in binOp(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("        /",a)
    #iterate for 3 remaining terms 
    if n == 3:
        r.add(c in for3terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("            /",a)
    #iterate for 4 remaining terms   
    if n == 4:
        r.add(c in for4terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("                /",a)
    return r.check() == sat

#returns TRUE if multiplying a helps achieve target with n other terms   
def findDivValWith(a, target, lst, n):
    c = float(target)/a
    r = Solver()
    #iterate for 2 remaining terms 
    if n == 2:
        r.add(c in binOp(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("        *",a)
    #iterate for 3 remaining terms   
    if n == 3:
        r.add(c in for3terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("            *",a)
    #iterate for 4 remaining terms   
    if n == 4:
        r.add(c in for4terms(c, removeFrom(a, lst)))
        if r.check() == sat:
            print("                *",a)
    return r.check() == sat
