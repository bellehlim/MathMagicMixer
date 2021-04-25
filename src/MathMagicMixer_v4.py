from z3 import *

ops = [ "*", "-", "+", "/" ]

#checks if x is an element in l
def oneOf(x, l):
    return Or([ x == p for p in l ])

#checks if the given _target_ value is attainable with a binary operation between _a_ and _b_
def binOp(target, a, o1, b):
    a, b = Reals('a b')
    return Or(And(o1 == '*', a * b == target),
              And(o1 == '/', a / b == target),
              And(o1 == '-', a - b == target),
              And(o1 == '+', a + b == target))

#checks if the given _target_ value is attainable with binary operations between (_a_ and _b_) and _c_
def triOp(target, a, o1, b, o2, c):
    r1, r2 = Reals('r1 r2')
    r1 = target
    r2 = c
    return Or(And(o2 == '*', binOp(r1 / r2, a, o1, b)),
              And(o2 == '/', binOp(r1 * r2, a, o1, b)),
              And(o2 == '-', binOp(r1 + r2, a, o1, b)),
              And(o2 == '+', binOp(r1 - r2, a, o1, b)))

#checks if the given _target_ value is attainable with binary operations between ((_a_ and _b_) and _c_) and _d_
def quadOp(target, a, o1, b, o2, c, o3, d):
    r1, r2 = Reals('r1 r2')
    r1 = target
    r2 = d
    return Or(And(o3 == '*', triOp(r1 / r2, a, o1, b, o2, c)),
              And(o3 == '/', triOp(r1 * r2, a, o1, b, o2, c)),
              And(o3 == '-', triOp(r1 + r2, a, o1, b, o2, c)),
              And(o3 == '+', triOp(r1 - r2, a, o1, b, o2, c)))

#checks if the given _target_ value is attainable with binary operations between (((_a_ and _b_) and _c_) and _d_) and _e_
def pentaOp(target, a, o1, b, o2, c, o3, d, o4, e):
    r1, r2 = Reals('r1 r2')
    r1 = target
    r2 = e
    return Or(And(o4 == '*', quadOp(r1 / r2, a, o1, b, o2, c, o3, d)),
              And(o4 == '/', quadOp(r1 * r2, a, o1, b, o2, c, o3, d)),
              And(o4 == '-', quadOp(r1 + r2, a, o1, b, o2, c, o3, d)),
              And(o4 == '+', quadOp(r1 - r2, a, o1, b, o2, c, o3, d)))

#NOT CURRENTLY USED -- will use when trying to allow for cases of duplicate dice (ex. [1, 1, 2, 4, 5])
#returns the list with _a_ removed (once) if present
def removeIfPresent(a, lst):
    if a in lst:
        lst.remove(a)
        return lst
    else:
        return lst

#NOT CURRENTLY USED -- will use when trying to allow for cases of duplicate dice (ex. [1, 1, 2, 4, 5])
#checks each of the five items matches to 1 instance in the given list
def our_distinct(a, b, c, d, e, given):
    z = And(a in given,
               b in removeIfPresent(a, given),
               c in removeIfPresent(b, removeIfPresent(a, given)),
               d in removeIfPresent(c, removeIfPresent(b, removeIfPresent(a, given))),
               e in removeIfPresent(d, removeIfPresent(c, removeIfPresent(b, removeIfPresent(a, given)))))
    print(z)
    return z

#main -- provide it the target number of list of 5 other numbers          
def findSolutions(target, given):
    a, b, c, d, e = Reals('a b c d e')
    o1, o2, o3, o4 = Strings('o1 o2 o3 o4')
    t = Solver()
    t.add(pentaOp(target, a, o1, b, o2, c, o3, d, o4, e),
          oneOf(a, given),
          oneOf(b, given),
          oneOf(c, given),
          oneOf(d, given),
          oneOf(e, given),
          oneOf(o1, ops),
          oneOf(o2, ops),
          oneOf(o3, ops),
          oneOf(o4, ops),
          Distinct(a, b, c, d, e))
          #our_distinct(a, b, c, d, e, given))
    while t.check() == sat:
        n1 = t.model()[a]
        n2 = t.model()[b]
        n3 = t.model()[c]
        n4 = t.model()[d]
        n5 = t.model()[e]
        op1 = as_string(t.model()[o1])
        op2 = as_string(t.model()[o2])
        op3 = as_string(t.model()[o3])
        op4 = as_string(t.model()[o4])
        print ("((((", n1, op1, n2, ")", op2, n3, ")", op3, n4, ")", op4, n5, ")")
        t.add(Not(And(a == t.model()[a],
                      b == t.model()[b],
                      c == t.model()[c],
                      d == t.model()[d],
                      e == t.model()[e],
                      o1 == t.model()[o1],
                      o2 == t.model()[o2],
                      o3 == t.model()[o3],
                      o4 == t.model()[o4])))
    print("done")

#removes quotation marks from accessed string item in array when printing (ex. instead of printing (3 "*" 2), print (3 * 2))     
#Taken from Z3Py documentation:
#https://z3prover.github.io/api/html/classz3py_1_1_seq_ref.html#aed8194b891258fc0b90afdc8ca371eaa
def as_string(self):
         """Return a string representation of sequence expression."""
         if self.is_string_value():
             string_length = ctypes.c_uint()
             chars = Z3_get_lstring(self.ctx_ref(), self.as_ast(), byref(string_length))
             return string_at(chars, size=string_length.value).decode('latin-1')
         return Z3_ast_to_string(self.ctx_ref(), self.as_ast())
