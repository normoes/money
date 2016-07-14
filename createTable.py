import os
import datetime
from utils.database import Database
from utils.inputClient import getCsvReader, checkDate

from utils.MoneyExceptions import *

"""
functions in sqlite
    http://pythoncentral.io/advanced-sqlite-usage-in-python/

uupdate delete insertmany
rollback any change since last commit
    db.rollback()

"""
    
def createTable(databaseName='',tableName='', debug = False):
    if not tableName:
        print 'no table name given'
        raise NoTableNameGivenException
    if not databaseName:
        print 'no database name given'
        raise NoDatabaseNameGivenException
    database = Database(name=databaseName, debug=debug)
    schema = ("CREATE TABLE "+ tableName +
              "(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"                      
              "created DATE NOT NULL,"
              "value REAL NOT NULL)")
	      #,"
              #"category TEXT,"
              #"description TEXT NOT NULL)")
    
    database.createTable(schema)
        
if __name__ == '__main__':
    databaseName = 'money.db'
    tableName = 'cash_portugal'
    createTable(databaseName=databaseName,tableName=tableName, debug = True)
