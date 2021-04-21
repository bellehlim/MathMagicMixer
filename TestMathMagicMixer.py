#Test oneOf
def testOneOf():
    assert oneOf(2, [1, 2, 3]) == Or(False, True, False)
    assert oneOf(4, [1, 2, 3]) == Or(False, False, False)
    assert oneOf(4, [4, 4, 4]) == Or(True, True, True)
    assert not oneOf(4, [1, 2, 3]) == Or(False, False, True)

#Test binOp
def testBinOp():
    assert binOp(24, [4,6]) == [24]
    assert binOp(12, [4,3]) == [12]
    assert not binOp(6, [4,3]) == [6]
    assert binOp(6, [4,3]) == []

#Test removeFrom
def testRemoveFrom():
    assert removeFrom(3, [1, 2, 4, 5, 3, 11]) == [1, 2, 4, 5, 11]
    assert removeFrom(3, [41, 56, 57, 101]) == [41, 56, 57, 101]
    assert removeFrom(3, []) == []

#Test for3terms
def testFor3Terms():
    assert for3terms(24, [3, 1, 6]) == [24]
    assert for3terms(9, [1, 2, 3]) == [9]
    assert not for3terms(24, [3, 1, 5]) == [24]
    assert for3terms(24, [3, 1, 5]) == []

#Test oneIterFor3
def testOneIterFor3():
    assert oneIterFor3(3, 21, [2,5]) == True
    assert oneIterFor3(3, 22, [2,5]) == False
    assert oneIterFor3(3, 21, [2,4,1]) == False

#Test for4terms
def testFor4Terms():
    assert for4terms(11, [1,3,5,2]) == [11, 11, 11, 11]
    assert for4terms(15, [1,3,5,2]) == [15, 15, 15]
    assert for4terms(45, [1,3,5,2]) == [45, 45]
    assert for4terms(63, [1,3,5,2]) == []
    assert not for4terms(41, [1,3,5,2]) == [41]

#Test oneIterFor4
def testOneIterFor4():
    assert oneIterFor4(3, 11, [1, 2, 4, 5]) == True
    assert oneIterFor4(3, 11, [1, 2, 4, 5, 6]) == True
    assert oneIterFor4(3, 73, [1, 2, 4, 5]) == False
    assert oneIterFor4(3, 97, [1, 2, 4, 5, 6]) == False

#Test for5terms
def testFor5Terms():
    assert for5terms(31, [1, 2, 3, 4, 5]) == [31, 31, 31, 31, 31]
    assert for5terms(21, [1, 2, 3, 4, 6]) == [21, 21, 21, 21, 21]
    assert not for5terms(71, [1, 2, 3, 4, 5]) == [71]
    assert not for5terms(24, [1, 2, 3, 4, 5]) == None

#Test findAddValWith
def testFindAddValWith():
    assert findAddValWith(3, 34, [1, 4], 2) == False
    assert findAddValWith(3, 21, [4, 5,3], 4) == False
    assert findAddValWith(3, 12, [4, 5], 1) == True

#Test findSubValWith
def testFindSubValWith():
    assert findSubValWith(21, 15, [6, 4], 1) == True
    assert findSubValWith(21, 15, [6, 4], 2) == False
    assert findSubValWith(21, 11, [6, 4, 1], 3) == False
    
#Test findDivValWith
def testFindDivValWith():
    assert findDivValWith(1,5,[2,3,4],2) == True
    assert findDivValWith(4,2,[2,5,3],1) == True
    assert findDivValWith(4,7,[12,5,3],2) == False

#Test findMulValWith
def testFindMulValWith():
    assert findMulValWith(4,7,[12,5,3],2) == False
    assert findMulValWith(2,16,[8,5,8],3) == True
    assert findMulValWith(3,21,[7,5,4,9],4) == True
    
#Will print "Everything passed" if none of the test fails
if __name__ == "__main__":
    testOneOf()
    testBinOp()
    testRemoveFrom()
    testFor3Terms()
    testOneIterFor3()
    testFor4Terms()
    testOneIterFor4()
    testFor5Terms()
    testFindAddValWith()
    testFindSubValWith()
    testFindDivValWith()
    testFindMulValWith()
    print("Everything passed")
