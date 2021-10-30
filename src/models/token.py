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