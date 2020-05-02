## See Documentation for PLY :
## https://www.dabeaz.com/ply/ply.html
##
## See also Documentation on Python in General :
## Built-in Functions (https://docs.python.org/3/library/functions.html#globals)
## Learn Python Programming (https://pythonbasics.org/)
## An Informal Introduction to Python (https://docs.python.org/2/tutorial/introduction.html#)
##
## To debug a Python Program in IDLE, do the following :
## 1. Select Menu Item "Run|Python Shell"
## 2. A Python Shell Window will open.
## 3. In Python Shell, select Menu Item "Debug|Debugger"
## 4. The Debug Control Window will appear.
## 5. Return to the IDLE IDE, Select Menu Item "Run|Run Module".
##
## To learn more about how to debug a Python Program in IDLE,
## see : Debugging program in idle ide of python
## https://www.youtube.com/watch?v=AKmdfFpN5BM
##
import ply.lex as lexmodule
import sys

tokens = [
    "SET",
    "GET",
    "ADD",
    "SUB",    
    "EXIT",
    "ASSIGN",
    "COMMA",
    "NAME",
    "INT",
    "NEWLINE"
]

## See PLY documentation : 4.3 Specification of tokens
## for information on how the PLY Framework determine how a PLY Module
## define the Regular Expressions associated with its List of Tokens.
t_ASSIGN = r'\='
t_COMMA = r','
t_ignore = " \t"  ## This is important in order to skip over spaces and tabs.

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    ## Unlike t_newline() of DemoPLY.py, t_NEWLINE does return a value
    ## because we want to detect a newline character.
    return t

def t_INT(t) :
    r'\d+'  ## This line is the function documentation string. In the case of PLY, it also serves as the Regular Expression of the INT token.
    t.value = int(t.value)
    ## The now modified "t" is returned.
    ## This directly affects the return
    ## value of Lexer.token().    
    return t

def t_NAME(t) :
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    ## See PLY Documentation Section : 4.3 Specification of tokens
    ## starting at line that reads :
    ## To handle reserved words, you should write a single rule...
    if (t.value == "SET") or (t.value == "GET") \
    or (t.value == "ADD") or (t.value == "SUB") \
    or (t.value == "EXIT"):
        t.type = t.value
    else:
        t.type = 'NAME'
    ## The now modified "t" is returned.
    ## This directly affects the return
    ## value of Lexer.token().        
    return t

def t_error(t) :
    print("Illegal Characters : [" + t.value + "]")
    t.lexer.skip(1)

def t_COMMENT(t):
    ## The regular expression below specifies a string that starts with ## or // followed by zero or more occurrences of any character (excpet newline)
    ## (that's what the .* indicates).
    ## Hence if PLY comes across a string that fits the above RegEx, the whole string (which is a comment) is treated as a token.
    ## See Python RegEx (https://www.w3schools.com/python/python_regex.asp).
    ##
    ## Also see PLY documentation 4.5 Discarded tokens
    ##
    r'[\#\#|//].*'  
    print("Single line comment : [" + t.value + "] Length : " + str(len(t.value)))
    pass
    ## No return value. Token discarded.
    ## This function does not return any value.
    ## This directly affects Lexer.token() in
    ## that Lexer.token() will skip this token
    ## and move onto the next token.

## See Documentation Section 9. Classes
## https://docs.python.org/3/tutorial/classes.html
class NameValue:
    name = ""
    value = 0
    
    def __init__(self, name, value):
        self.name = name
        self.value = int(value)

    ## See str() vs repr() in Python
    ## https://www.geeksforgeeks.org/str-vs-repr-in-python/
    ## and
    ## __str__ vs. __repr__
    ## https://www.pythonforbeginners.com/basics/__str__-vs-__repr
    ##
    def __str__(self):
        return 'NameValue(%s,%d)' % (self.name, self.value)

    def __repr__(self):
        return str(self)    

listNVPairs = []

def GetNameValue(theName):
    ## Check listNVPairs to see if
    ## a NameValue instance with name
    ## matching theName exits in the list.
    for nv in listNVPairs:
        if (nv.name == theName):
            return nv        
    return None

def SetNameValue(nameValue):
    bFound = False
    for i in range(len(listNVPairs)):
        if (listNVPairs[i].name == nameValue.name):
            listNVPairs[i] = nameValue
            bFound = True
            break
    if (bFound == False):
        listNVPairs.append(nameValue)

def iterate_tokens(theLexer):
    while True:
        tok = theLexer.token()
        if not tok:
            break
        print(tok)

def iterate_token_regex():
    ## Iterate over a list in Python
    ## https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
    ##
    ## Note in the PLY Documentation :
    ## When a function is used to specify a Regular Expression, the regular expression rule is specified in the function documentation string.
    ## To see the Regular Expression of a Token Function, use Python Docstrings (https://www.geeksforgeeks.org/python-docstrings/)
    ##
    print("The following lists the Regular Expressions of Each Token :")
    for tok in tokens:
        print(tok, end=" : ")  ## See : How to print without newline in Python? (https://www.geeksforgeeks.org/print-without-newline-python/)
        if (tok == "SET"):
            print("SET")
        elif (tok == "GET"):
            print("GET")
        elif (tok == "ADD"):
            print("ADD")
        elif (tok == "SUB"):
            print("SUB")
        elif (tok == "EXIT"):
            print("EXIT")            
        elif callable(eval("t_" + tok)):
            print(eval("t_" + tok).__doc__)
        else:        
            print(globals()["t_" + tok]) 

## The purpose of SkipAllTokensInLine() is to skip over all
## tokens until the NEWLINE is encountered.
def SkipAllTokensInLine(theLexer):
    while True:
        tok = theLexer.token()
        if not tok:
            break                
        elif (tok.type == "NEWLINE"):
            break

def run_interpreter(theLexer, content):
    returnValue = None
    theLexer.input(content)
    while True:
        tok = theLexer.token()        
        ## This must be the first "if" condition,
        ## otherwise if "tok" is None, then tok.<anything>
        ## will cause an exception.
        if not tok:
            returnValue = None
            break

        print("tok.type == [" + tok.type + "]")
        ## Note that because NEWLINE is now processed
        ## and a LexToken is returned in t_NEWLINE(),
        ## tok.type == "NEWLINE" is possible.
        ## But if so, it will be ignored in the code
        ## that follow below.
        
        if tok.type == "SET":
            ## Get next token.
            tok = theLexer.token()
            ## Must be a NAME.
            if (tok == None) or (tok.type != "NAME"):
                print("Syntax error. A NAME Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            theName = tok.value
            print("Name : [" + theName + "]")

            ## Get next token.
            tok = theLexer.token()
            ## Must be an ASSIGN.
            if (tok == None) or (tok.type != "ASSIGN"):
                print("Syntax error. An ASSIGN Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            ## Get next token.
            tok = theLexer.token()
            ## Must be a NAME or an INT 
            if (tok == None) or ((tok.type != "NAME") and (tok.type != "INT")):
                print("Syntax error. A NAME or INT Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            if (tok.type == "NAME"):
                nameValueExisting = GetNameValue(tok.value)
                if (nameValueExisting == None):
                    print("Error. Name : [" + tok.value + "] Not Found")
                else:
                    SetNameValue(NameValue(theName,
                      int(nameValueExisting.value)))
            elif (tok.type == "INT"):
                SetNameValue(NameValue(theName, int(tok.value)))

            SkipAllTokensInLine(theLexer)
            
        elif tok.type == "GET":
            ## Get next token.
            tok = theLexer.token()
            ## Must be a NAME.
            if (tok == None) or (tok.type != "NAME"):
                print("Syntax error. A NAME is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            nameValueExisting = GetNameValue(tok.value)
            if (nameValueExisting == None):
                print("Error. Name : [" + tok.value + "] Not Found")
            else:
                print("NAME [" + nameValueExisting.name + "] Value : [" + str(nameValueExisting.value) + "]")

            SkipAllTokensInLine(theLexer)

        elif tok.type == "ADD":
            ## Get next token.
            tok = theLexer.token()
            ## Must be a NAME.
            if (tok == None) or (tok.type != "NAME"):
                print("Syntax error. A NAME Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            nameValueTarget = GetNameValue(tok.value)
            if (nameValueTarget == None):
                print("Syntax Error. Name [" + tok.value + "] Not Found.")
                SkipAllTokensInLine(theLexer)
                continue
            else:
                print("Name : [" + nameValueTarget.name + "] Current Value : [" + str(nameValueTarget.value) + "]")

            ## Get next token.
            tok = theLexer.token()
            ## Must be a COMMA.
            if (tok == None) or (tok.type != "COMMA"):
                print("Syntax error. A COMMA Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            ## Get next token.
            tok = theLexer.token()
            ## Must be a NAME or an INT 
            if (tok == None) or ((tok.type != "NAME") and (tok.type != "INT")):
                print("Syntax error. A NAME or INT Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            if (tok.type == "NAME"):
                nameValueSource = GetNameValue(tok.value)
                if (nameValueSource == None):
                    print("Syntax Error. Name : [" + tok.value + "] Not Found")                    
                else:
                    nameValueTarget.value += nameValueSource.value
                    SetNameValue(nameValueTarget)
            elif (tok.type == "INT"):
                nameValueTarget.value += int(tok.value)
                SetNameValue(nameValueTarget)

            SkipAllTokensInLine(theLexer)
            
        elif tok.type == "SUB":
            ## Get next token.
            tok = theLexer.token()
            ## Must be a NAME.
            if (tok == None) or (tok.type != "NAME"):
                print("Syntax error. A NAME Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            nameValueTarget = GetNameValue(tok.value)
            if (nameValueTarget == None):
                print("Syntax Error. Name [" + tok.value + "] Not Found.")
                SkipAllTokensInLine(theLexer)
                continue
            else:
                print("Name : [" + nameValueTarget.name + "] Current Value : [" + str(nameValueTarget.value) + "]")

            ## Get next token.
            tok = theLexer.token()
            ## Must be a COMMA.
            if (tok == None) or (tok.type != "COMMA"):
                print("Syntax error. A COMMA Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            ## Get next token.
            tok = theLexer.token()
            ## Must be a NAME or an INT 
            if (tok == None) or ((tok.type != "NAME") and (tok.type != "INT")):
                print("Syntax error. A NAME or INT Token is expected.")
                SkipAllTokensInLine(theLexer)
                continue

            if (tok.type == "NAME"):
                nameValueSource = GetNameValue(tok.value)
                if (nameValueSource == None):
                    print("Syntax Error. Name : [" + tok.value + "] Not Found")
                else:
                    nameValueTarget.value -= nameValueSource.value
                    SetNameValue(nameValueTarget)
            elif (tok.type == "INT"):
                nameValueTarget.value -= int(tok.value)
                SetNameValue(nameValueTarget)

            SkipAllTokensInLine(theLexer)

        elif tok.type == "EXIT":
            returnValue = tok
            SkipAllTokensInLine(theLexer)
            break

    return returnValue
    
    
## For more information on usage of Command Line arguments in Python, see : Python - Command Line Arguments
## https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(parameters):
    iterate_token_regex()
    ## The following is a call to the ply folder lex.py source
    ## file's lex() function.
    ## The return value is an instance of a Lexer class.
    lexer = lexmodule.lex()  
    if (len(parameters) > 0):
        filename = parameters[0]
        print(filename)
        with open(filename) as f:
            content = f.read()
        print("Now about to Scan through the following Document :")
        print(content)        
        run_interpreter(lexer, content)
    else:
        while True:
            try:
                print("\r\nPlease enter code below : ")
                ## To get input from the console, code : input()
                content = input()
                returnTok = run_interpreter(lexer, content)
                if(not returnTok):
                    continue
                else:
                    break
            except EOFError:
                break            

## Note that Python sequentially executes all non-indented source code lines
## that it encounters in a .py file.
## See : Python Main Function
## https://www.geeksforgeeks.org/python-main-function/            
## See also : Python main function
## https://www.journaldev.com/17752/python-main-function            
##            
## For more info on the meaning of __name__ in Python, see :
## __name__ (A Special variable) in Python
## https://www.geeksforgeeks.org/__name__-special-variable-python/            
if __name__ == "__main__":
    if (len(sys.argv) > 0):
        main(sys.argv[1:])
    else:
        main([])
                    ## To understand the meaning of [1:], see : Python: What does for x in A[1:] mean?
                    ## https://stackoverflow.com/questions/27652686/python-what-does-for-x-in-a1-mean
                    ## See also :
                    ## Understanding slice notation (https://stackoverflow.com/questions/509211/understanding-slice-notation)
                    ## Python Lists and List Slices (https://docs.python.org/2/tutorial/introduction.html#lists)\
                    ## 15 Extended Slices (https://docs.python.org/2.3/whatsnew/section-slices.html)

    
    
    

