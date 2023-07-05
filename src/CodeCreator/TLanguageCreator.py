#!/usr/bin/env python 
# encoding:utf-8
class TLanguageCreator(object):
    _key = ""
    _rets = ""

    def __init__(self):
        pass

    def dealRow(self, row, rowIdx, key):
        if (self._key != row[1].value):
            if (self._key == ""):
                # start
                self._rets += '\"' + row[1].value + '\" : {\n'
            else:
                # end pre
                self._rets = self._rets[:-2]
                self._rets += "\n"
                self._rets += "},\n"
                # start next
                self._rets += '\"' + row[1].value + '\" : {\n'
            self._key = row[1].value

        self._rets += '\"'+row[0].value + \
            '\" :\"' + row[rowIdx].value + "\",\n"

    def creatorsZHLanguage(self, ws, maxCol, maxRows):
        self._key = ""
        self._rets = "{\n"
        for row in ws.iter_rows(min_row=5, max_col=maxCol, max_row=maxRows + 1):
            if row[0].value == None:
                break

            self.dealRow(row, 2, "zh")

        self._rets = self._rets[:-2]
        self._rets += "\n"
        self._rets += "}}"

        return self._rets

    def creatorsENLanguage(self, ws, maxCol, maxRows):
        self._key = ""
        self._rets = "{\n"
        for row in ws.iter_rows(min_row=5, max_col=maxCol, max_row=maxRows + 1):
            if row[0].value == None:
                break

            self.dealRow(row, 3, "en")

        self._rets = self._rets[:-2]
        self._rets += "\n"
        self._rets += "}}"

        return self._rets
