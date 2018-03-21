#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# import os
# import datetime
from utils.database import Database
# from utils.input_client import get_csv_reader, check_date

from utils.dbConnect_deco import dbConnectAndClose
from utils.ExceptionsDeco import printException

"""
functions in sqlite
    http://pythoncentral.io/advanced-sqlite-usage-in-python/

uupdate delete insertmany
rollback any change since last commit
    db.rollback()

"""


class DbController():

    def __init__(self, database_name='money.db', debug=False):
        self.database_name = database_name
        self.debug = debug
        self.database = Database(name=database_name, debug=debug)


  @printException
  @dbConnectAndClose
  def create_table(self, table_name=''):
    if not table_name:
        print 'no table name given'
        raise NoTableNameGivenException
    if not self.database_name:
        print 'no database name given'
        raise NoDatabaseNameGivenException
    schema = ("CREATE TABLE "+ table_name +
              "(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
              "created DATE NOT NULL,"
              "value REAL NOT NULL,"
	      #,"
              "category TEXT,"
              "description TEXT NOT NULL)")
    print schema

    self.database.createTable(schema)


if __name__ == '__main__':
  dbCont = DbController(debug=True)
  dbCont.create_table(table_name='bitcoins')
  # databaseName = 'money_test.db'
  # tableName = 'anlagen_portugal'
  # createTable(databaseName=databaseName,tableName=tableName, debug = True)
