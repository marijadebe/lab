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
