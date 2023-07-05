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
        return TTypeToTSType.get(self._type)

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
        return len(self._keyList) == 1 and self._fieldList[0].getTargetType() == "number"

    def creatorDeclare(self):
        sRecord = "I" + self._name + "Record"
        sTale = self._name + "Txt"
        s = "export interface " + sRecord + " { \n"
        for aField in self._fieldList:
            s += "    // " + aField.getComment() + "\n"
            s += "    " + aField.getName() + ":" + aField.getTargetType() + "\n"
        s += "}\n"

        # ts export

        s += "export let " + sTale + " = {\n"

        paramStr_1 = ""
        paramStr_2 = "`"
        if (len(self._keyList) > 1):
            for ik in range(0, len(self._keyList)):
                paramStr_1 += self._fieldList[ik].getName(
                ) + ":" + self._fieldList[ik].getTargetType() + ","
                paramStr_2 += "${" + self._fieldList[ik].getName() + "}_"
            paramStr_1 = paramStr_1[:-1]
            paramStr_2 = paramStr_2[:-1] + "`"
        else:
            paramStr_1 = self._fieldList[0].getName(
            ) + ":" + self._fieldList[0].getTargetType()
            paramStr_2 = self._fieldList[0].getName()

        s += "    getDataByKey(" + paramStr_1 + "): " + \
            sRecord + "| undefined {\n"
        s += "        return map.get("+paramStr_2+");\n"
        s += "    },\n"
        s += "    getAllData() {\n"
        s += "        return map;\n"
        s += "    },\n"
        s += "};\n"

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
                for ik in range(0, len(self._keyList)):
                    key += str(row[ik].value) + "_"
                key = key[:-1]
                key = "\'" + str(key) + "\'"
            else:
                key = str(row[0].value)
            sRow = ""
            sRow += "map.set(" + str(key) + ",{"
            for icol in range(0, maxCol):
                sRow += self._fieldList[icol].getDataString(
                    row[icol].value) + ","

            sRow = sRow[:-1] + "});\n"
            s += sRow

        return s


# if __name__ == "__main__":
#     aClass = TTSClass("TxtTable")
#     print(aClass.getName()) 
