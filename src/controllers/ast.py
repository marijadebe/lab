from models.types import Types
from models.tree import Tree

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