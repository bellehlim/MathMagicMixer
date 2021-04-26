from z3 import *

ops = [ "*", "-", "+", "/" ]

#checks if x is an element in l
def oneOf(x, l):
    return Or([ x == p for p in l ])


#checks if the broken down expression equals the target
def exprToTarget(target, exprArray):
    expr = String('expr')
    val = Int('val')
    newArray = []
    newArray.extend(exprArray)
    exprConcat = " ".join(newArray)
    val = eval(exprConcat)
    return val == target

#main -- provide it the target number of list of 5 other numbers          
def findSolutions(target, given):
    a, b, c, d, e = Reals('a b c d e')
    o1, o2, o3, o4 = Strings('o1 o2 o3 o4')
    n1, n2, n3, n4, n5 = Strings('n1 n2 n3 n4 n5')
    t = Solver()

    t.add(oneOf(a, given),
          oneOf(b, given),
          oneOf(c, given),
          oneOf(d, given),
          oneOf(e, given),
          oneOf(o1, ops),
          oneOf(o2, ops),
          oneOf(o3, ops),
          oneOf(o4, ops),
          Distinct(a, b, c, d, e))
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
        if exprToTarget(target, [n1, op1, n2, op2, n3, op3, n4, op4, n5]):
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
