#----------------------------------------------------------------------
# classsearch.py
# Author: Lois I Omotara
#----------------------------------------------------------------------
import contextlib as cl
import sqlite3
#----------------------------------------------------------------------
DATABASE_URL = 'file:reg.sqlite?mode=ro'
class ClassSearch:
    def __init__ (self,classid):
        self._classid = classid

    def __execute__(self, str):
        with sqlite3.connect(DATABASE_URL , isolation_level= None,
            uri= True) as connection:
            with cl.closing(connection.cursor()) as cursor:
                cursor.execute(str, [self._classid])
                return cursor.fetchall()
    def get_general(self):
        stm_str = "SELECT courses.courseid, classes.days, "
        stm_str+= "classes.starttime, classes.endtime,"
        stm_str += " classes.bldg, classes.roomnum,"
        stm_str += " courses.area, courses.title, courses.descrip, "
        stm_str += "courses.prereqs FROM courses, classes"
        stm_str += " WHERE courses.courseid=classes.courseid"
        stm_str += " AND classes.classid LIKE ?"
        general = self.__execute__(stm_str)
        return general
    def get_deptandnum(self):
        stm_str="SELECT crosslistings.dept, crosslistings.coursenum"
        stm_str+=" FROM crosslistings, classes"
        stm_str+=" WHERE crosslistings.courseid=classes.courseid"
        stm_str+=" AND classes.classid LIKE ? ORDER BY dept ASC, "
        stm_str+="coursenum ASC"
        return self.__execute__(stm_str)
    def get_prof(self):
        stm_str="SELECT profs.profname FROM coursesprofs, profs,"
        stm_str+="classes WHERE coursesprofs.profid=profs.profid"
        stm_str+=" AND classes.courseid=coursesprofs.courseid"
        stm_str+=" AND classid LIKE ? ORDER BY profname ASC"
        return self.__execute__(stm_str)
