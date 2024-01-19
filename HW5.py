#!/usr/bin/env python3

# WRITE YOUR NAME and YOUR COLLABORATORS HERE
# Name: Ian McLerran
# Collaborators: None

import re

# global variables:
opstack = []  #assuming top of the stack is the end of the list
dictstack = []  #assuming top of the stack is the end of the list
operators = {}
scopetype = "dynamic"

# debugging:
isDebug = False

# regex:
reTokens = r'/?[a-zA-Z][a-zA-Z0-9_]*|[\[][a-zA-Z-?0-9_\s!][a-zA-Z-?0-9_\s!]*[\]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]'
reOperators = r'(add)|(sub)|(mul)|(eq)|(lt)|(gt)|(length)|(get)|(put)|(aload)|(astore)|(dup)|(copy)|(count)|(pop)|(clear)|(exch)|(stack)|(dict)|(begin)|(end)|(def)|(if)|(ifelse)|(for)'
reNames = r'/?[a-zA-Z][a-zA-Z0-9_]*'
reNumbers = r'[-]?[0-9]+'
reArray = r'[\[][a-zA-Z-?0-9_\s!][a-zA-Z-?0-9_\s!]*[\]]'
reArrayElems = r'[\[\]]+|/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+'
reWhitespace = r'[\s]+'

# OPSTACK MANIPULATION:
#------------------------------------------------------------------------------
def opPop():
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.
    if len(opstack) != 0:
        op = opstack.pop()
        while str == type(op):
            if '/' is not op[0]:
                if("static" == scopetype):
                    op = lookupStat(op)
                else:
                    op = lookupDyn(op)
            else:
                break
        return op
    return opstack

def opPush(value):
    opstack.append(value)

# DICTSTACK MANIPULATION:
#------------------------------------------------------------------------------
def dictPop():
    if len(dictstack) != 0:
        return dictstack.pop()
    return dictstack

def dictPush(d,link):
    dictstack.append((link,d))

def define(name, value):
    if len(dictstack) == 0:
        dictPush({},0)
    dictstack[-1][1][name] = value

def lookupDyn(name):
    name2 = name
    if name[0] is not '/':
        name2 = '/' + name
    else:
        name2 = name[1:]
    for i, d in list(reversed(dictstack)):
        if name in d.keys():
            return d[name]
        if name2 in d.keys():
            return d[name2]
    raise Exception("Error: the name '{}' does not exist in any dictionary in the dictstack.".format(name))

def lookupStat(name):
    name2 = name
    if name[0] is not '/':
        name2 = '/' + name
    else:
        name2 = name[1:]
    dictTup = dictstack[-1]
    link = dictTup[0]
    if name in dictTup[1]:
        return dictTup[1][name]
    elif name2 in dictTup[1]:
        return dictTup[1][name2]
    while dictTup != dictstack[link]:
        dictTup = dictstack[link]
        link = dictTup[1]
        if name in dictTup[1]:
            return dictTup[1][name]
        if name2 in dictTup[1]:
            return dictTup[1][name2]
    raise Exception("Error: the name '{}' could not be found in the current scope.".format(name))

# HELPER METHODS:
#------------------------------------------------------------------------------
def isNumber(x):
    return ( isinstance(x, (int, float, complex)) and not isinstance(x, bool) )

def isArray(a):
    return (isinstance(a, tuple) and isNumber(a[0]) and isinstance(a[1], list))

# ARITHMETIC AND COMPARISON OPERATORS:
#------------------------------------------------------------------------------
def add():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `add` operation. Insufficient operands on the opstack: Expected 2, but found {}.".format(len(opstack)))
    op1 = opPop()
    op2 = opPop()
    if not isNumber(op1):
        raise Exception("Error: Cannot perform `add` operation. '{}' is not a number.".format(op1))
    if not isNumber(op2):
        raise Exception("Error: Cannot perform `add` operation. '{}' is not a number.".format(op2))
    opPush(op2 + op1)

def sub():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `sub` operation. Insufficient operands on the opstack: Expected 2, but found {}.".format(len(opstack)))
    op1 = opPop()
    op2 = opPop()
    if not isNumber(op1):
        raise Exception("Error: Cannot perform `sub` operation. '{}' is not a number".format(op1))
    if not isNumber(op2):
        raise Exception("Error: Cannot perform `sub` operation. '{}' is not a number.".format(op2))
    opPush(op2 - op1)

def mul():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `mul` operation. Insufficient operands on the opstack: Expected 2, but found {}.".format(len(opstack)))
    op1 = opPop()
    op2 = opPop()
    if not isNumber(op1):
        raise Exception("Error: Cannot perform `mul` operation. '{}' is not a number.".format(op1))
    if not isNumber(op2):
        raise Exception("Error: Cannot perform `mul` operation. '{}' is not a number.".format(op2))
    opPush(op2 * op1)

def eq():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `eq` operation. Insufficient operands on the opstack: Expected 2, but found {}".format(len(opstack)))
    op1 = opPop()
    op2 = opPop()
    opPush(op2 == op1)

def lt():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `lt` operation. Insufficient operands on the stack: Expected 2, but found {}.".format(len(opstack)))
    op1 = opPop()
    op2 = opPop()
    if not isNumber(op1):
        raise Exception("Error: Cannot perform `lt` operation. '{}' is not a number.".format(op1))
    if not isNumber(op2):
        raise Exception("Error: Cannot perform `lt` operation. '{}' is not a number.".format(op2))
    opPush(op2 < op1)

def gt():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `gt` operation. Insufficient operands on the stack: Expected 2, but found {}.".format(len(opstack)))
    op1 = opPop()
    op2 = opPop()
    if not isNumber(op1):
        raise Exception("Error: Cannot perform `gt` operation. '{}' is not a number.".format(op1))
    if not isNumber(op2):
        raise Exception("Error: Cannot perform `gt` operation. '{}' is not a number.".format(op2))
    opPush(op2 > op1)

# ARRAY OPERATORS:
#------------------------------------------------------------------------------
def length():
    if len(opstack) == 0:
        raise Exception("Error: Cannot perform `length` operation. Insufficient operands on the stack: Expected 1, but found 0.")
    arrTuple = opPop()
    if not isArray(arrTuple):
        raise Exception("Error: Cannot perform `length` operation. '{}' is not an array.".format(arrTuple))
    opPush(arrTuple[0])

def get():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `get` operation. Insufficient operands on the stack: Expected 2, but found {}.".format(len(opstack)))
    index = opPop()
    arrTuple = opPop()
    if not isNumber(index):
        raise Exception("Error: Cannot perform `get` operation. '{}' is not a number.".format(index))
    if not isArray(arrTuple):
        raise Exception("Error: Cannot perform `get` operation. '{}' is not an array.".format(arrTuple))
    if index >= arrTuple[0]:
        raise Exception("Error: Cannot perform `get` operation. Index {} is out of bounds.".format(index))
    opPush(arrTuple[1][index])

def put():
    if len(opstack) < 3:
        raise Exception("Error: Cannot perform `put` operation. Insufficient operands on the stack: Expected 3, but found {}.".format(len(opstack)))
    value = opPop()
    index = opPop()
    arrTuple = opPop()
    if not isNumber(index):
        raise Exception("Error: Cannot perform `put` operation. '{}' is not a number.".format(index))
    if not isArray(arrTuple):
        raise Exception("Error: Cannot perform `put` operation. '{}' is not an array.".format(arrTuple))
    if index >= arrTuple[0]:
        raise Exception("Error: Cannot perform `put` operation. Index {} is out of bounds.".format(index))
    arrTuple[1][index] = value

def aload():
    if len(opstack) == 0:
        raise Exception("Error: Cannot perform `aload` operation. Insufficient operands on the stack: Expected 1, but found 0.")
    arrTuple = opPop()
    if not isArray(arrTuple):
        raise Exception("Error: Cannot perform `aload` operation. '{}' is not an array.".format(arrTuple))
    for e in arrTuple[1]:
        opPush(e)
    opPush(arrTuple)

def astore():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `astore` operation. Insufficient operands on the stack: Expected (at least) 2, but found {}.".format(len(opstack)))
    arrTuple = opPop()
    if not isArray(arrTuple):
        raise Exception("Error: Cannot perform `astore` operation. '{}' is not an array.".format(arrTuple))
    if len(opstack) < arrTuple[0]:
        raise Exception("Error: Cannot perform `astore` operation. Insufficient operands on the stack: Expected {}, but found {}.".format(arrTuple[0],len(opstack)))
    arrLen = arrTuple[0]
    for i in range(arrLen):
        arrTuple[1][arrLen - i - 1] = opPop()
    opPush(arrTuple)

# STACK OPERATORS:
#------------------------------------------------------------------------------
def dup():
    if len(opstack) == 0:
        raise Exception("Error: Cannot perform `dup` operation. Insufficient operands on the stack: Expected 1, but found 0.")
    op1 = opPop()
    opPush(op1)
    opPush(op1)

def copy():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `copy` operation. Insufficient operands on the stack: Expected (at least) 2, but found {}.".format(len(opstack)))
    n = opPop()
    if len(opstack) < n:
        raise Exception("Error: Cannot perform `copy` operation. Insufficient operands on the stack: Expected {}, but found {}.".format(n, len(opstack)))
    opCopies = []
    for i in range(n):
        opCopies.append(opPop())
    opCopies.reverse()
    for op in opCopies:
        opPush(op)
    for op in opCopies:
        opPush(op)

def count():
    opPush(len(opstack))

def pop():
    opPop()

def clear():
    opstack[:] = []

def exch():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `exch` operation. Insufficient operands on the stack: Expected 2, but found {}.".format(len(opstack)))
    op1 = opPop()
    op2 = opPop()
    opPush(op1)
    opPush(op2)

# TODO: modify stack to meet requirements
def stack():
    print("==============")
    if len(opstack) < 1:
        print("The opstack is empty.")
    else:
        for op in list(reversed(opstack)):
            if isArray(op):
                print(op[1])
            else:
                print(op)
    print("==============")
    if len(dictstack) == 0:
        print("The dictstack is empty.")
    else:
        for i in range(len(dictstack)-1, -1, -1):
            print("{{---- {} ---- {} ----}}".format(i, dictstack[i][0]))
            for k in dictstack[i][1].keys():
                print("{}    {}".format(k,dictstack[i][1][k]))
    print("==============")

# DICTIONARY OPERATORS:
#------------------------------------------------------------------------------

def psDef():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform def operation. Insufficient operands on the stack: Expected 2, but found {}.".format(len(opstack)))
    value = opPop()
    name = opPop()
    define(name, value)

# CONDITIONAL AND LOOP OPERATORS:
#------------------------------------------------------------------------------
# Add a scope argument to the the following functions
# TODO: psIf
# TODO: psIfelse
# TODO: psFor

def psFor():
    if len(opstack) < 4:
        raise Exception("Error: Cannot perform `for` operation. Insufficient operands on the opstack: Expected 3, but found {}.".format(len(opstack)))
    code = opPop()
    final = opPop()
    incr = opPop()
    init = opPop()
    if not isNumber(init):
        raise Exception("Error: Cannot perform `for` operation. Expected a number at argument 1, but found {}.".format(init))
    if not isNumber(incr):
        raise Exception("Error: Cannot perform `for` operation. Expected a number at argument 2, but found {}.".format(incr))
    if not isNumber(final):
        raise Exception("Error: Cannot perform `for` operation. Expected a number at argument 3, but found {}.".format(final))
    if list is not type(code):
        raise Exception("Error: Cannot perform `for` operation. Expected a code array at argument 4, but found {}.".format(code))
    if incr >= 0:
        x = init
        while(x <= final):
            opPush(x)
            interpretSPS(code, scopetype)
            x += incr
    else:
        x = init
        while(x >= final):
            opPush(x)
            interpretSPS(code, scopetype)
            x += incr

def psIf():
    if len(opstack) < 2:
        raise Exception("Error: Cannot perform `if` operation. Insufficient operands on the opstack: Expected 2, but found {}.".format(len(opstack)))
    code = opPop()
    isTrue = opPop()
    if bool is not type(isTrue):
        raise Exception("Error: Cannot perform `if` operation. Expected a boolean value at argument 1, but found {}.".format(isTrue))
    if list is not type(code):
        raise Exception("Error: Cannot perform `if` operation. Expected a code array at argument 2, but found {}.".format(code))
    if isTrue:
        interpretSPS(code, scopetype)

def ifElse():
    if len(opstack) < 3:
        raise Exception("Error: Cannot perform `ifElse` operation. Insufficient operands on the opstack: Expected 3, but found {}.".format(len(opstack)))
    falseCode = opPop()
    trueCode = opPop()
    isTrue = opPop()
    if bool is not type(isTrue):
        raise Exception("Error: Cannot perform `ifElse` operation. Expected a boolean value at argument 1, but found {}.".format(isTrue))
    if list is not type(trueCode):
        raise Exception("Error: Cannot perform `ifElse` operation. Expected a code array at argument 2, but found {}.".format(trueCode))
    if list is not type(falseCode):
        raise Exception("Error: Cannot perform `ifElse` operation. Expected a code array at argument 3, but found {}.".format(falseCode))
    if isTrue:
        interpretSPS(trueCode, scopetype)
    else:
        interpretSPS(falseCode, scopetype)


# ------ SSPS functions -----------
# search the dictstack for the dictionary "name" is defined in and return the (list) index for that dictionary (start searhing at the top of the stack)
def staticLink(name):
    name2 = name
    if name[0] is not '/':
        name2 = '/' + name
    else:
        name2 = name[1:]
    dictTup = dictstack[-1]
    link = dictTup[0]
    if name in dictTup[1]:
        return len(dictstack)-1
    elif name2 in dictTup[1]:
        return len(dictstack)-1
    while dictTup != dictstack[link]:
        dictTup = dictstack[link]
        link = dictTup[0]
        if name in dictTup[1]:
            return link
        if name2 in dictTup[1]:
            return link
    raise Exception("Error: the name '{}' could not be found in the current scope.".format(name))

def tokenize(s):
    return re.findall(reTokens, s)

def groupMatch(it):
    res = []
    for c in it:
        if c == '}':
            return res
        elif c=='{':
            innerRes = groupMatch(it)
            if(False == innerRes):
                return False
            res.append(innerRes)
        else:
            res.append(parseToken(c))
    return False

def parse(L):
    res = []
    it = iter(L)
    for c in it:
        if c=='}':  #non matching closing parenthesis; return false since there is
                    # a syntax error in the Postscript code.
            return False
        elif c=='{':
            innerRes = groupMatch(it)
            if(False == innerRes):
                return False
            res.append(innerRes)
        else:
            res.append(parseToken(c))

    return res

# convert string tokens to code representation
def parseToken(c):
    if 'true' == c:
        return True
    if 'false' == c:
        return False
    if re.match(reNumbers, c):
        return int(c)
    if re.match(reArray, c):
        return parseArray(c)
    return c

# rework?
# parse array should be changed to be called during interpretation instead of during parsing?
def parseArray(a):
    arrLen = 0
    arrArr = []
    toks = re.findall(reArrayElems, a)
    toks.remove('[')
    toks.remove(']')
    it = iter(toks)
    for c in it:
        arrLen += 1
        if 'true' == c:
            arrArr.append(True)
        elif 'false' == c:
            arrArr.append(False)
        elif '' == c:
            arrLen -= 1
        elif re.match(reWhitespace, c):
            arrLen -= 1
        elif re.match(reNumbers, c):
            arrArr.append(int(c))
        else:
            arrArr.append(c)
    return (arrLen, arrArr)

#the main recursive interpreter function
def interpretSPS(tokenL,scope):
    for c in tokenL:
        #debug
        if isDebug:
            print("---------------------") #debug
            print("=> {}".format(c))
            stack()
            print("---------------------") #debug
        #/debug
        if type(c) is str:
            if('/' == c[0]): #c is a name
                opPush(c)
                if isDebug:
                    print("pushing '{}' to stack.".format(c)) #debug
            elif re.match(reOperators, c):
                res = operators[c]
                res()
            else:
                res = None
                if "static" == scope:
                    res = lookupStat(c)
                elif "dynamic" == scope:
                    res = lookupDyn(c)
                else:
                    raise Exception("Error: Invalid scope type.")
                if callable(res): #c is an operator
                    raise Exception("""This code should never be excecuted, since design has been changed so that built in operators are no longer stored in dictstack.
                                       This change contradicts standard PostScript design (built in operators are the first dict in stack), but has been added to support 
                                       unit tests for SSPS.""")
                    res()
                elif list is type(res): #c is  function (code array)
                    link = len(dictstack) - 1
                    if("static" == scope):
                        link = staticLink(c)
                    dictPush({}, link)
                    interpretSPS(res,scope)
                    dictPop()
                else:
                    opPush(res) #c is a variable
                    if isDebug:
                        print("pushing '{}' to stack.".format(res)) #debug
        else:
            opPush(c) #c is any other operand, such as a number or boolean
            if isDebug:
                print("pushing '{}' to stack.".format(c)) #debug

#parses the input string and calls the recursive interpreter to solve the
#program
def interpreter(s, scope):
    global scopetype
    scopetype = scope
    clearBoth()
    initBuiltInOps()
    tokenL = parse(tokenize(s))
    interpretSPS(tokenL,scope)

#clears both stacks
def clearBoth():
    opstack[:] = []
    dictstack[:] = []

def initBuiltInOps():
    dictPush({},0)

    operators['add'] = add
    operators['sub'] = sub
    operators['mul'] = mul
    operators['eq'] = eq
    operators['lt'] = lt
    operators['gt'] = gt
    operators['length'] = length
    operators['get'] = get
    operators['put'] = put
    operators['aload'] = aload
    operators['astore'] = astore
    operators['dup'] = dup
    operators['copy'] = copy
    operators['count'] = count
    operators['pop'] = pop
    operators['clear'] = clear
    operators['exch'] = exch
    operators['def'] = psDef
    operators['stack'] = stack
    operators['for'] = psFor
    operators['if'] = psIf
    operators['ifelse'] = ifElse

