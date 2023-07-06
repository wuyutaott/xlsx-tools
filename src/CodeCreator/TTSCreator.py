from CodeCreator.TBaseCreator import TBaseCreator, TBaseField

TTypeToTSType = {
    "int": "number",
    "string": "string",
    "list<int>": "Array<number>",
    "list<string>": "Array<string>",
    "list<list<int>>": "Array<Array<number>>",
    "list<list<string>>": "Array<Array<string>>",
}


class TTSField(TBaseField):
    def getTargetType(self):        
        value = TTypeToTSType.get(self._type)
        if value == None:
            print("字段数据配型配置错误", self._name, self._type)
        return value

    def dealLineChar(self, sData):
        sData = sData.replace("\n", "\\n").replace("\"", "\\\"")
        return sData

    def getDataString(self, sData):
        if (sData == None):
            sData = ""
        sData = str(sData)

        ret = ""
        if (self._type == "int"):
            ret = sData
        if (self._type == "string"):
            sData = self.dealLineChar(sData)
            ret = "\"" + str(sData) + "\""
        # , 分隔
        if (self._type == "list<int>"):
            sList = sData.split(",")
            ret = "["
            for s in sList:
                ret += s + ","

            ret = ret[:-1]
            ret += "]"
        # ,; 分隔
        if (self._type == "list<list<string>>"):
            sList_1 = sData.split(";")
            ret = "["
            for subS_1 in sList_1:
                sList_2 = subS_1.split(",")
                ret += "["
                s = ""
                for subS_2 in sList_2:
                    subS_2 = self.dealLineChar(subS_2)
                    s += "\"" + str(subS_2) + "\","

                ret += s[:-1]
                ret += "],"
            ret = ret[:-1]
            ret += "]"

        if (self._type == "list<list<int>>"):
            sList_1 = sData.split(";")
            ret = "["
            for subS_1 in sList_1:
                sList_2 = subS_1.split(",")
                ret += "["
                s = ""
                for subS_2 in sList_2:
                    subS_2 = self.dealLineChar(subS_2)
                    s += str(subS_2) + ","

                ret += s[:-1]
                ret += "],"
            ret = ret[:-1]
            ret += "]"
        if (self._type == "list<string>"):
            sList = sData.split(",")
            ret = "["
            for s in sList:
                s = self.dealLineChar(s)
                ret += "\"" + str(s) + "\","

            ret = ret[:-1]
            ret += "]"

        return self._name + ":" + ret


class TTSCreator(TBaseCreator):

    def __init__(self, name=None, fieldList=None, keyList=None):
        super().init(name, fieldList, keyList)
        self._fileSuffix = "Txt.ts"

    def creatorField(self, name, sType, comment):
        return TTSField(name, sType, comment)

    def keyIsNumber(self):
        if len(self._keyList) == 1:
            index = self._keyList[0]
            type = self._fieldList[index].getTargetType()
            if type == "number":
                return True
        return False        

    def creatorDeclare(self):
        """
        创建声明
        1.创建字段定义
        2.创建工具函数
        """
        sRecord = "I" + self._name + "Record"
        sTale = self._name + "Txt"
       
        # 创建字段定义
        s = "export interface " + sRecord + " { \n"
        for aField in self._fieldList:
            s += "    // " + aField.getComment() + "\n"     # 字段注释
            s += "    " + aField.getName() + ": "           # 字段名称
            s += aField.getTargetType() + "\n"              # 字段类型
        s += "}\n"

        # 创建工具函数
        s += "\nexport let " + sTale + " = {\n"
        paramStr = ""       # getDataByKey函数参数
        mapKeyStr = "`"     # map.get函数参数
        if (len(self._keyList) == 0):
            print("错误：配置表没有配置主键")
            return ""
        elif (len(self._keyList) > 1): # 多主键
            for ik in self._keyList:
                paramStr += self._fieldList[ik].getName() + ": " + self._fieldList[ik].getTargetType() + ", "
                mapKeyStr += "${" + self._fieldList[ik].getName() + "}_"
            paramStr = paramStr[:-2]
            mapKeyStr = mapKeyStr[:-1] + "`"
        else: # 单主键
            index = self._keyList[0] # 主键字段索引
            paramStr = self._fieldList[index].getName() + ": " + self._fieldList[index].getTargetType()
            mapKeyStr = self._fieldList[index].getName()

        s += "    getDataByKey(" + paramStr + "): " + \
            sRecord + " | undefined {\n"
        s += "        return map.get(" + mapKeyStr + ");\n"
        s += "    },\n\n"
        s += "    getAllData() {\n"
        s += "        return map;\n"
        s += "    },\n"
        s += "};\n\n"

        return s

    def creatorData(self, ws, maxCol, maxRows):
        s = ""
        sRecord = "I" + self._name + "Record"
        if self.keyIsNumber():
            s += "let map: Map<number, " + sRecord + \
                "> = new Map<number, " + sRecord + ">();\n"
        else:
            s += "let map: Map<string, " + sRecord + \
                "> = new Map<string, " + sRecord + ">();\n"

        sRow = ""
        for row in ws.iter_rows(min_row=self._dataStartRow, max_col=maxCol, max_row=maxRows + 1):
            if row[0].value == None:
                break
            key = ""
            if not self.keyIsNumber():
                for index in self._keyList:
                    key += str(row[index].value) + "_"
                key = key[:-1]
                key = "\'" + str(key) + "\'"
            else:
                index = self._keyList[0]
                key = str(row[index].value)
            sRow = ""
            sRow += "map.set(" + str(key) + ",{"
            for icol in range(0, maxCol):
                sRow += self._fieldList[icol].getDataString(
                    row[icol].value) + ","

            sRow = sRow[:-1] + "});\n"
            s += sRow

        return s
