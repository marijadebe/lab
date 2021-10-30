from enum import Enum
import sys
import re

from models.token import Token
from models.tree import Tree
from models.types import Types
from controllers.lexer import lexer

#Abstract syntax tree
def ast(tokenarr):
    hiearchy = []
    for x in range(len(tokenarr)):
        if((tokenarr[x][0].getType() == Types.IDENTIFIER and (1 < len(tokenarr[x])) and tokenarr[x][1].getValue() == "=") or tokenarr[x][0].getType() == Types.FUNCTION or tokenarr[x][0].getType() == Types.LOOP or tokenarr[x][0].getType() == Types.LOOPDELIMITER):
            hiearchy.append(Tree(tokenarr[x][0]))
            y = 1
            while ((y < len(tokenarr[x])) and not(tokenarr[x][y].getType() == Types.IDENTIFIER and ((y+1 < len(tokenarr[x])) and tokenarr[x][y+1].getValue() == "=")) and tokenarr[x][y].getType() != Types.FUNCTION and tokenarr[x][y].getType() != Types.LOOP and tokenarr[x][y].getType() != Types.LOOPDELIMITER):
                if(tokenarr[x][y].getValue() != "=" and tokenarr[x][y].getType() != Types.COMMENT):
                    hiearchy[-1].addChild(tokenarr[x][y])
                y+=1

    return hiearchy.copy()

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
                print("")
                for j in range(len(astree[x].children)):
                    if astree[x].getChild(j).getToken().getType() == Types.STRING:
                        sys.stdout.write(astree[x].getChild(j).getToken().getValue())
                    elif astree[x].getChild(j).getToken().getType() == Types.IDENTIFIER:
                        sys.stdout.write(variables[astree[x].getChild(j).getToken().getValue()])
                    elif astree[x].getChild(j).getToken().getType() == Types.ARGUMENT:
                        val = re.findall('[0-9]+',astree[x].getChild(j).getToken().getValue())
                        val = int(val[0])
                        sys.stdout.write(str(sys.argv[val+2]))
        elif astree[x].getToken().getType() == Types.IDENTIFIER:
            dump = astree[x].children.copy() 
            evalstring = ""
            condition = ""
            for z in range(len(dump)):
                if dump[z].getToken().getType() == Types.SEPARATION:
                    if(dump[z].getToken().getValue() == "?"):
                        condition = eval(evalstring)
                        if (condition):
                            if dump[z+2].getToken().getType() == Types.IDENTIFIER:
                                variables[astree[x].getToken().getValue()] = str(variables[dump[z+2].getToken().getValue()])
                            else:
                                variables[astree[x].getToken().getValue()] = str(dump[z+2].getToken().getValue())
                        else:
                            if dump[z+4].getToken().getType() == Types.IDENTIFIER:
                                variables[astree[x].getToken().getValue()] = str(variables[dump[z+4].getToken().getValue()])
                            else:
                                variables[astree[x].getToken().getValue()] = str(dump[z+4].getToken().getValue())
                        break
                if(dump[z].getToken().getType() == Types.IDENTIFIER):
                    evalstring += variables[dump[z].getToken().getValue()]
                elif(dump[z].getToken().getType() == Types.ARGUMENT):
                    val = re.findall('[0-9]+',dump[z].getToken().getValue())
                    val = int(val[0])
                    evalstring += str(sys.argv[val+2])
                else:
                    evalstring += str(dump[z].getToken().getValue())
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