from models.types import Types

def initVariableDict(tree, dictionary):
    for x in range(len(tree)):
        if tree[x].getToken().getType() == Types.IDENTIFIER and (len(tree[x].children) == 1) and dictionary.get(tree[x].getToken().getValue()) == None:
            if tree[x].getChild(0).getToken().getType() == Types.STRING:
                dictionary[tree[x].getToken().getValue()] = tree[x].getChild(0).getToken().getValue().strip("\n")
            if tree[x].getChild(0).getToken().getType() == Types.INTEGER:
                #Tilde signifies integer
                dictionary[tree[x].getToken().getValue()] = "~"+tree[x].getChild(0).getToken().getValue().strip("\n")
        if tree[x].getToken().getType() == Types.IDENTIFIER and len(tree[x].children) > 1 and dictionary.get(tree[x].getToken().getValue()) == None:
            dictionary[tree[x].getToken().getValue()] = "~0"