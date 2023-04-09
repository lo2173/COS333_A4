#-----------------------------------------------------------------------
# Author: Lois I Omotara
# lineparser.py
#-----------------------------------------------------------------------

class LineParser:
    def __init__(self,array):
        self._line = array
    def getclassid(self):
        classid = self._line[0]
        return classid
    def getdept(self):
        dept = self._line[1]
        return dept
    def getnum(self):
        number = self._line[2]
        return number
    def getarea(self):
        return self._line[3]
    def gettitle(self):
        return self._line[4]
