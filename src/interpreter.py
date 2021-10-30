from enum import Enum
import sys
import re

from models.token import Token
from models.tree import Tree
from models.types import Types
from controllers.lexer import lexer
from controllers.ast import ast
from controllers.out import out

#Interpreter
def interpreter(astree):
    variables = {}
    looping = 0
    x = 0
    while x < len(astree):
        if (astree[x].getToken().getType() == Types.LOOP):
            interstring = ""
            looping = 1
            for i in range(len(astree[x].children)):
                dite = astree[x].getChild(i).getToken() 
                if(dite.getType() == Types.IDENTIFIER):
                    interstring += variables[dite.getValue()]
                else:
                    interstring += dite.getValue()
            if  (not eval(interstring)):
                looping = 0
                while(astree[x].getToken().getType() != Types.LOOPDELIMITER):
                    x = x + 1
        if (astree[x].getToken().getType() == Types.LOOPDELIMITER):
            if looping == 1:
                x = x - 1
                while (astree[x+1].getToken().getType() != Types.LOOP):
                    x = x - 1
        elif (astree[x].getToken().getType() == Types.FUNCTION):
            if(astree[x].getToken().getValue() == "out"):
                out(astree[x], variables)
        elif astree[x].getToken().getType() == Types.IDENTIFIER:
            dump = astree[x].children.copy() 
            evalstring = ""
            condition = ""
            z = 0
            while z < len(dump):
                if dump[z].getToken().getType() == Types.SEPARATION:
                    if(dump[z].getToken().getValue() == "?" and dump[z].getToken().getType() == Types.SEPARATION):
                        evalstring2 = ""
                        condition = eval(evalstring)
                        if (condition):
                            z+=1
                            while not(dump[z].getToken().getType() == Types.SEPARATION and dump[z].getToken().getValue() == ":"):
                                if dump[z].getToken().getType() == Types.IDENTIFIER:
                                    evalstring2 += str(variables[dump[z].getToken().getValue()])
                                else:
                                    evalstring2 += str(dump[z].getToken().getValue())
                                z+=1
                            variables[astree[x].getToken().getValue()] = str(eval(evalstring2))
                        else:
                            z+=1
                            while not(dump[z-1].getToken().getType() == Types.SEPARATION and dump[z-1].getToken().getValue() == ":"):
                                z+=1
                            while z < len(dump):
                                if dump[z].getToken().getType() == Types.IDENTIFIER:
                                    evalstring2 += str(variables[dump[z].getToken().getValue()])
                                else:
                                    evalstring2 += str(dump[z].getToken().getValue())
                                z+=1
                            variables[astree[x].getToken().getValue()] = str(eval(evalstring2))
                        break
                if(dump[z].getToken().getType() == Types.IDENTIFIER):
                    evalstring += variables[dump[z].getToken().getValue()]
                elif(dump[z].getToken().getType() == Types.ARGUMENT):
                    val = re.findall('[0-9]+',dump[z].getToken().getValue())
                    val = int(val[0])
                    evalstring += str(sys.argv[val+2])
                else:
                    evalstring += str(dump[z].getToken().getValue())
                z += 1
            if (condition == ""):
                if re.search("[a-z]", evalstring):
                    output = eval('"'+evalstring+'"')
                else:
                    output = eval(evalstring)
                variables[astree[x].getToken().getValue()] = str(output)
        x+=1
def main():
    tokens = lexer(sys.argv[1])
    astree = ast(tokens)
    interpreter(astree)

main()