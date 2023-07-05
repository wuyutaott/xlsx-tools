class TFormulaCreator(object): 
    def __init__(self):
        pass

    def toLua(self, row):
        funcName = row[1].value
        paramList = row[2].value
        formulaStr = row[3].value

        s = "TxtFormula."+funcName + "= function(" + paramList+")\n"
        formulaStr = formulaStr.replace("pow", "math.pow")
        formulaStr = formulaStr.replace("ceil", "math.ceil")
        formulaStr = formulaStr.replace("random", "math.random")
        s += "return " + formulaStr + "\n" + "end" + "\n"

        return s

    def creatorLua(self, ws, maxCol, maxRows):
        s = "TxtFormula = {}\n"
        for row in ws.iter_rows(min_row=3, max_col=maxCol, max_row=maxRows + 1):
            if row[0].value == None:
                break

            s += self.toLua(row)

        return s

    def toTS(self, row):
        funcName = row[1].value
        paramList = row[2].value
        formulaStr = row[3].value

        s = funcName + ": function(" + paramList+"){\n"
        formulaStr = formulaStr.replace("pow", "Math.pow")
        formulaStr = formulaStr.replace("ceil", "Math.ceil")
        formulaStr = formulaStr.replace("random", "Math.random")
        s += "return " + formulaStr + "\n},\n"
        return s

    def creatorTS(self, ws, maxCol, maxRows):
        s = "export let TxtFormula = {\n"
        for row in ws.iter_rows(min_row=3, max_col=maxCol, max_row=maxRows + 1):
            if row[0].value == None:
                break
            s += self.toTS(row)

        s += "}\n"
        return s
