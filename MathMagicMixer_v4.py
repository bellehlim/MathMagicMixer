from z3 import *
s = SolverFor("LIA")

ops = [ "*", "-", "+", "/" ]

#checks if x is an element in l
def oneOf(x, l):
    return Or([ x == p for p in l ])

def secondTerm(target, a, o1, b):
    a, b = Reals('a b')
    #print("secondTerm")
    return Or(And(o1 == '*', a * b == target),
              And(o1 == '/', a / b == target),
              And(o1 == '+', a + b == target),
              And(o1 == '-', a - b == target))

def thirdTerm(target, a, o1, b, o2, c):
    r1, r2 = Reals('r1 r2')
    r1 = target
    r2 = c
    #print("thirdTerm")
    return Or(And(o2 == '*', secondTerm(r1 / r2, a, o1, b)),
              And(o2 == '/', secondTerm(r1 * r2, a, o1, b)),
              And(o2 == '+', secondTerm(r1 + r2, a, o1, b)),
              And(o2 == '-', secondTerm(r1 - r2, a, o1, b)))

def fourthTerm(target, a, o1, b, o2, c, o3, d):
    r1, r2 = Reals('r1 r2')
    r1 = target
    r2 = d
    #print("fourthTerm")
    return Or(And(o3 == '*', thirdTerm(r1 / r2, a, o1, b, o2, c)),
              And(o3 == '/', thirdTerm(r1 * r2, a, o1, b, o2, c)),
              And(o3 == '+', thirdTerm(r1 + r2, a, o1, b, o2, c)),
              And(o3 == '-', thirdTerm(r1 - r2, a, o1, b, o2, c)))

def fifthTerm(target, a, o1, b, o2, c, o3, d, o4, e):
    r1, r2 = Reals('r1 r2')
    r1 = target
    r2 = e
    #print("fifthTerm")
    return Or(And(o4 == '*', fourthTerm(r1 / r2, a, o1, b, o2, c, o3, d)),
              And(o4 == '/', fourthTerm(r1 * r2, a, o1, b, o2, c, o3, d)),
              And(o4 == '+', fourthTerm(r1 + r2, a, o1, b, o2, c, o3, d)),
              And(o4 == '-', fourthTerm(r1 - r2, a, o1, b, o2, c, o3, d)))

#main -- provide it the target number of list of 5 other numbers          
def findSolutions(target, given):
    a, b, c, d, e = Reals('a b c d e')
    o1, o2, o3, o4 = Strings('o1 o2 o3 o4')
    n1, n2, n3, n4, n5 = Strings('n1 n2 n3 n4 n5')
    t = Solver()
    t.add(fifthTerm(target, a, o1, b, o2, c, o3, d, o4, e),
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
    print("finished round")
    while t.check() == sat:
        n1 = str(t.model()[a].as_long())
        n2 = str(t.model()[b].as_long())
        n3 = str(t.model()[c].as_long())
        n4 = str(t.model()[d].as_long())
        n5 = str(t.model()[e].as_long())
        op1 = as_string(t.model()[o1])
        op2 = as_string(t.model()[o2])
        op3 = as_string(t.model()[o3])
        op4 = as_string(t.model()[o4])
        print (n1, op1, n2, op2, n3, op3, n4, op4, n5)
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
        
    
def as_string(self):
         """Return a string representation of sequence expression."""
         if self.is_string_value():
             string_length = ctypes.c_uint()
             chars = Z3_get_lstring(self.ctx_ref(), self.as_ast(), byref(string_length))
             return string_at(chars, size=string_length.value).decode('latin-1')
         return Z3_ast_to_string(self.ctx_ref(), self.as_ast())
