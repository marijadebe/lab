import re

from models.token import Token
from models.types import Types

#Lexical analysis
def lexer(file):
    '''
    Returns an array of arrays (by lines in a file) of Token objects assign

            Parameters:
                    file (string): A file name of a format xxxx.lab

            Returns:
                    tokenarr (array): A 2-D array of Token objects
    '''
    
    tokenarr = []
    with open(file, encoding = 'utf-8') as f:
        lines = f.readlines()
        for x in range(len(lines)):
            mezzoarr = lines[x].split(" ")
            tokens = []
            y = 0
            while y < len(mezzoarr):
                if re.search("^[*+-\/=%<>]$|^==$|^&&$",mezzoarr[y]):
                    if re.search("^&&$", mezzoarr[y]):
                        tokens.append(Token(Types.OPERATOR, " and "))
                    else:    
                        tokens.append(Token(Types.OPERATOR, mezzoarr[y]))
                if re.search("^[0-9]+$",mezzoarr[y]):
                    tokens.append(Token(Types.INTEGER, mezzoarr[y]))
                if re.search("^[0-9]+\.[0-9]+$", mezzoarr[y]):
                    tokens.append(Token(Types.FLOAT, mezzoarr[y]))
                if re.search('^".*',mezzoarr[y]):
                    retezec = ""
                    while(True):
                        str = ""
                        if not re.search('^".*',mezzoarr[y]):
                            str = " "
                        retezec += str+mezzoarr[y]
                        if (re.search('.*"$', mezzoarr[y])):
                            break
                        y+=1
                    tokens.append(Token(Types.STRING, retezec.strip('\n').strip('"')))
                    if(y+1 >= len(mezzoarr)):
                        break
                    else:
                        y+=1
                if re.search('^\/\/[^\/].*', mezzoarr[y]):
                    tokens.append(Token(Types.COMMENT, mezzoarr[y].strip('\n')))
                    while(y < len(mezzoarr)):
                        tokens.append(Token(Types.COMMENT, mezzoarr[y].strip('\n')))
                        y+=1
                    break
                if re.search('^\?$|^:$', mezzoarr[y]):
                    tokens.append(Token(Types.SEPARATION, mezzoarr[y]))
                if re.search("^while", mezzoarr[y]):
                    tokens.append(Token(Types.LOOP, mezzoarr[y]))
                elif re.search("^elihw", mezzoarr[y]):
                    tokens.append(Token(Types.LOOPDELIMITER, mezzoarr[y]))
                elif (mezzoarr[y] == "out"):
                    tokens.append(Token(Types.FUNCTION, mezzoarr[y]))
                elif re.search('^arg\[[0-9].*\]$', mezzoarr[y]):
                    tokens.append(Token(Types.ARGUMENT, mezzoarr[y]))
                elif re.search('^[^"123456789+\/*%-=<>].*', mezzoarr[y]):
                    tokens.append(Token(Types.IDENTIFIER, mezzoarr[y].strip('\n')))
                y+=1
            tokenarr.append(tokens.copy())
    return tokenarr