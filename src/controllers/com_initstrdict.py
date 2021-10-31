import random
import string
from models.types import Types
def initStringDict(tree, dictionary):
    for x in range(len(tree)):
            for y in range(len(tree[x].children)):
                if tree[x].getChild(y).getToken().getType() == Types.STRING and tree[x].getToken().getType() != Types.IDENTIFIER:
                    dictionary[tree[x].getChild(y).getToken().getValue()] = generateIdentifier(dictionary)
def generateIdentifier():
    randomIdentifier = ''.join(random.choices(string.ascii_letters, k=16))
    return randomIdentifier