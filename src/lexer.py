from enum import Enum
import sys
import re

#Classes
class Types(Enum):
    OPERATOR = 1
    INTEGER = 2
    STRING = 3
    IDENTIFIER = 4
    COMMENT = 5
    FUNCTION = 6
    ARGUMENT = 7
    FLOAT = 8
    SEPARATION = 9

class Token():
    def __init__(self,type, value):
        self.__type = type
        self.__value = value
    def getType(self):
        return self.__type
    def getValue(self):
        return self.__value
    def setType(self,type):
        self.__type=type
    def setValue(self, value):
        self.__value = value

class Tree():
    children = []
    def __init__(self,token):
        self.__token = token
        self.children = []
    def addChild(self,token):
        self.children.append(Tree(token))
    def getChild(self,index):
        return self.children[index]
    def getToken(self):
        return self.__token
    def setToken(self, token):
        self.__token = token

#Lexical analysis
def lexer():
    tokenarr = []
    with open(sys.argv[1], encoding = 'utf-8') as f:
        lines = f.readlines()
        for x in range(len(lines)):
            mezzoarr = lines[x].split(" ")
            tokens = []
            for y in range(len(mezzoarr)):
                if re.search("^[*+-\/=%<>]$|^==$",mezzoarr[y]):
                    tokens.append(Token(Types.OPERATOR, mezzoarr[y]))
                if re.search("^[0-9]+$",mezzoarr[y]):
                    tokens.append(Token(Types.INTEGER, mezzoarr[y]))
                if re.search("^[0-9]+\.[0-9]+$", mezzoarr[y]):
                    tokens.append(Token(Types.FLOAT, mezzoarr[y]))
                if re.search('^".*"$',mezzoarr[y]):
                    tokens.append(Token(Types.STRING, mezzoarr[y].strip('\n').strip('"')))
                if re.search('^\/\/[^\/].*', mezzoarr[y]):
                    tokens.append(Token(Types.COMMENT, mezzoarr[y].strip('\n')))
                    while(y < len(mezzoarr)):
                        tokens.append(Token(Types.COMMENT, mezzoarr[y].strip('\n')))
                        y+=1
                    break
                if re.search('^\?$|^:$', mezzoarr[y]):
                    tokens.append(Token(Types.SEPARATION, mezzoarr[y]))
                if (mezzoarr[y] == "out"):
                    tokens.append(Token(Types.FUNCTION, mezzoarr[y]))
                elif re.search('^arg\[[0-9].*\]$', mezzoarr[y]):
                    tokens.append(Token(Types.ARGUMENT, mezzoarr[y]))
                elif re.search('^[^"123456789+\/*%-=<>].*', mezzoarr[y]):
                    tokens.append(Token(Types.IDENTIFIER, mezzoarr[y].strip('\n')))
            tokenarr.append(tokens.copy())
    return tokenarr

#Abstract syntax tree
def ast(tokenarr):
    hiearchy = []
    for x in range(len(tokenarr)):
        if((tokenarr[x][0].getType() == Types.IDENTIFIER and (1 < len(tokenarr[x])) and tokenarr[x][1].getValue() == "=") or tokenarr[x][0].getType() == Types.FUNCTION):
            hiearchy.append(Tree(tokenarr[x][0]))
            y = 1
            while ((y < len(tokenarr[x])) and not(tokenarr[x][y].getType() == Types.IDENTIFIER and ((y+1 < len(tokenarr[x])) and tokenarr[x][y+1].getValue() == "=")) and tokenarr[x][y].getType() != Types.FUNCTION):
                if(tokenarr[x][y].getValue() != "=" and tokenarr[x][y].getType() != Types.COMMENT):
                    hiearchy[-1].addChild(tokenarr[x][y])
                y+=1
    return hiearchy.copy()

#Interpreter
def interpreter(astree):
    variables = {}
    for x in range(len(astree)):
        if (astree[x].getToken().getType() == Types.FUNCTION):
            if(astree[x].getToken().getValue() == "out"):
                for j in range(len(astree[x].children)):
                    if astree[x].getChild(j).getToken().getType() == Types.STRING:
                        print(astree[x].getChild(j).getToken().getValue())
                    elif astree[x].getChild(j).getToken().getType() == Types.IDENTIFIER:
                        print(variables[astree[x].getChild(j).getToken().getValue()])
                    elif astree[x].getChild(j).getToken().getType() == Types.ARGUMENT:
                        val = re.findall('[0-9]+',astree[x].getChild(j).getToken().getValue())
                        val = int(val[0])
                        print(str(sys.argv[val+2]))
        if astree[x].getToken().getType() == Types.IDENTIFIER:
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

def main():
    tokens = lexer()
    astree = ast(tokens)
    interpreter(astree)

main()