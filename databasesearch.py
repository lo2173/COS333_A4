#----------------------------------------------------------------------
# databasesearch.py
# Author: Lois I Omotara
#----------------------------------------------------------------------
import sqlite3
import contextlib as cl

DATABASE_URL = 'file:reg.sqlite?mode=ro'
class DatabaseSearch:
    def __init__(self):
        self._stmt_str = "SELECT classes.classid, crosslistings.dept,"
        self._stmt_str+=" crosslistings.coursenum,courses.area,"
        self._stmt_str+= " courses.title FROM courses, classes, "
        self._stmt_str+="crosslistings "
        self._stmt_str+="WHERE classes.courseid=courses.courseid"
        self._stmt_str+=" AND courses.courseid=crosslistings.courseid"
        self._replace_list = []
    def __escapewilds__(self, field):
        if (field.find('%') >= 0 ) or (field.find('_') >= 0):
            self._stmt_str += " ESCAPE '^'"
        newfield = field.replace('%', '^%')
        newfield = newfield.replace('_', "^_")
        return newfield
    def __addwilds__(self, field):
        newfield = "%"+field+"%"
        return newfield
    def deptsearch(self, dept):
        if dept is None:
            return
        self._stmt_str+=" AND crosslistings.dept LIKE ?"
        deptfield = self.__escapewilds__(dept)
        deptfield = self.__addwilds__(deptfield)
        self._replace_list.append(deptfield)
        return
    def numsearch(self, num):
        if num is None:
            return
        self._stmt_str += " AND crosslistings.coursenum LIKE ?"
        numfield = self.__escapewilds__(num)
        numfield = self.__addwilds__(numfield)
        self._replace_list.append(numfield)
        return
    def areasearch(self, area):
        if area is None:
            return
        self._stmt_str += " AND courses.area LIKE ?"
        areafield = self.__escapewilds__(area)
        areafield = self.__addwilds__(areafield)
        self._replace_list.append(areafield)
        return
    def titlesearch(self, title):
        if title is None:
            return
        self._stmt_str+=" AND courses.title LIKE ?"
        titlefield = self.__escapewilds__(title)
        titlefield = self.__addwilds__(titlefield)
        self._replace_list.append(titlefield)
        return
    def get_replacelist(self):
        return self._replace_list
    def get_cmdstring(self):
        return self._stmt_str
    def execute(self):
        with sqlite3.connect(DATABASE_URL , isolation_level= None,
            uri= True) as connection:
            with cl.closing(connection.cursor()) as cursor:
                self._stmt_str+=" ORDER BY crosslistings.dept ASC"
                self._stmt_str+=''', crosslistings.coursenum ASC,
                 classes.classid ASC'''
                cursor.execute(self._stmt_str, self._replace_list)
                return cursor.fetchall()
    def fullsearch(self, idept, iarea, icoursenum, ititle):
        self.deptsearch(dept=idept)
        self.areasearch(area=iarea)
        self.numsearch(num=icoursenum)
        self.titlesearch(title = ititle)
        return self.execute()
    def getall(self):
        with sqlite3.connect(DATABASE_URL , isolation_level= None,
            uri= True) as connection:
            with cl.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT classes.classid, crosslistings.dept,"
                stmt_str+=" crosslistings.coursenum,courses.area,"
                stmt_str+= " courses.title FROM courses, classes, "
                stmt_str+="crosslistings "
                cursor.execute(stmt_str)
                return cursor.fetchall()
            