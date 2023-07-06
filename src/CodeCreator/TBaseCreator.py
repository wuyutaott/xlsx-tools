import abc 


class TBaseField(object):
    _name = ""
    _type = ""
    _comment = ""

    def __init__(self, name, sType, comment):
        self._name = name
        self._type = sType
        self._comment = comment        

    def getComment(self):
        return self._comment

    def getName(self):
        return self._name

    @abc.abstractclassmethod
    def getTargetType(self):
        pass

    @abc.abstractclassmethod
    def getDataString(self, sData):
        pass


class TBaseCreator(object):
    # 类名
    _name = None
    # 字段
    _fieldList = None
    # key
    _keyList = None

    # 到处文件后缀名
    _fileSuffix = ""

    _dataStartRow = 5

    def __init__(self, name=None, fieldList=None, keyList=None):
        self._name = name
        self._fieldList = fieldList
        self._keyList = keyList

    def init(self, name, fieldList, keyList):
        self._name = name
        self._fieldList = fieldList
        self._keyList = keyList

    def getName(self):
        return self._name

    def getFieldList(self):
        return self._fieldList

    def getKeyList(self):
        return self._keyList

    def getFileSuffix(self):
        return self._fileSuffix

    @abc.abstractclassmethod
    def creatorField(self, name, sType, comment):
        return None

    @abc.abstractclassmethod
    def creatorDeclare(self):
        """
        创建数据声明部分
        """
        return ""

    @abc.abstractclassmethod
    def creatorData(self, ws, maxCol, maxRows):
        """
        创建数据部分
        """
        return ""

    def ceatorAllCode(self, ws, maxCol, maxRows):
        s = "// DO NOT EDIT! This is a generated file.\n"
        s += "\n"        
        s += self.creatorDeclare()
        s += self.creatorData(ws, maxCol, maxRows)
        return s
