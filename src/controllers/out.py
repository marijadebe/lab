import sys
import re

from models.types import Types

def out(treechildren, variables):
    print("")
    for j in range(len(treechildren.children)):
        if treechildren.getChild(j).getToken().getType() == Types.STRING:
            sys.stdout.write(treechildren.getChild(j).getToken().getValue())
        elif treechildren.getChild(j).getToken().getType() == Types.IDENTIFIER:
            sys.stdout.write(variables[treechildren.getChild(j).getToken().getValue()])
        elif treechildren.getChild(j).getToken().getType() == Types.ARGUMENT:
            val = re.findall('[0-9]+',treechildren.getChild(j).getToken().getValue())
            val = int(val[0])
            sys.stdout.write(str(sys.argv[val+2]))