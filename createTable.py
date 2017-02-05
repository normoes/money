#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os
import datetime
from utils.database import Database
from utils.inputClient import getCsvReader, checkDate

from utils.MoneyExceptions import *

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

  def __init__(self, databaseName='money.db', debug=False):
    self.databaseName = databaseName
    self.debug = debug
    self.db = Database(name=databaseName, debug=debug)

  @printException
  @dbConnectAndClose
  def createTable(self, tableName=''):
    if not tableName:
        print 'no table name given'
        raise NoTableNameGivenException
    if not self.databaseName:
        print 'no database name given'
        raise NoDatabaseNameGivenException
    schema = ("CREATE TABLE "+ tableName +
              "(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
              "created DATE NOT NULL,"
              "value REAL NOT NULL,"
	      #,"
              "category TEXT,"
              "description TEXT NOT NULL)")
    print schema

    self.db.createTable(schema)

if __name__ == '__main__':
  dbCont = DbController(debug=True)
  dbCont.createTable(tableName='rawmaterials_portugal')
  #databaseName = 'money_test.db'
  #tableName = 'anlagen_portugal'
  #createTable(databaseName=databaseName,tableName=tableName, debug = True)
