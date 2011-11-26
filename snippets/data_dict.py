# The following function will print the data dictionary for the given table
# Usage :-> python data_dict.py host_name user_name password db_name
# Dependencies : python and xlwt ( python module for excel )
import MySQLdb
import sys
import os

# try to import xlwt or raise an error
try :
    from xlwt import *
except :
    print "You do not have python xlwt installed"
    sys.exit()


class DataDict():
    """ class to create a data dictionary for the given database """
    def __init__(self):
        # get the current working directory
        self.CWD = os.path.dirname(__file__)

    def get_db(self,args):
        """get the arguments from command line"""
        try :
            host = args[1]
            user = args[2]
            password = args[3]
            db = args[4]
        except :
            print "Usage : python data_dict.py host_name user_name password db_name"
            print "Exp   : python data_dict.py localhost pratz pratz@123 test_db"
            sys.exit()

        # try to connect to database
        try :
            self.con = MySQLdb.connect(host,user,password,db)
            self.cur = self.con.cursor()
        except Exception, e :
            print "Error connecting to Database"
            print e
            sys.exit()

    def get_tables(self) :
        """ get all the tables for the given database """
        self.cur.execute("show tables;")
        tables = self.cur.fetchall()
        return [ table[0] for table in tables]

    def get_table_desc(self,tables_list):
        """ get the table description """
        desc_dict = {}
        for table in tables_list :
            self.cur.execute("desc " + table)
            desc_dict[table] = self.cur.fetchall()
        return desc_dict

    def write_datadict(self, desc_dict):
        """ method to write to excel file """

        # sort the dict
        desc_list =  sorted(desc_dict.keys())

        # define a work book
        work_book = Workbook()
        work_sheet = work_book.add_sheet('Data Dictionary')

        # define bold font to headers
        head_font = Font()
        head_font.bold = True

        # define a style
        head_style = XFStyle()
        head_style.font = head_font

        header_list = ['Field','Type','Null','Key','Default','Extra']
        # define the headers for the excel file
        head_col_count = 0
        for header in header_list :
            work_sheet.write(0,head_col_count,header,head_style)
            head_col_count = head_col_count + 1

        row_count = 1
        for table in desc_list :
            work_sheet.write(row_count,0,table,head_style)
            row_count = row_count + 1
            for desc in desc_dict[table] :
                col_count = 0
                for item in desc :
                    work_sheet.write(row_count,col_count,item)
                    col_count = col_count + 1
                row_count = row_count + 1
            row_count = row_count + 1

        # join the current path and file name
        path = os.path.join(self.CWD,'Data_Dictionary.xls')
        work_book.save(path)


if __name__ == '__main__' :
    dd = DataDict()
    dd.get_db(sys.argv)
    desc_dict = dd.get_table_desc(dd.get_tables())
    dd.write_datadict(desc_dict)
    print "Success ! A file named Data_Dictionary.xls is created in your current directory"
