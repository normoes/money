from utils.sqlite3_db import SQLlite_DB
from utils.dbConnect_deco import dbConnectAndClose

"""
TODO (see TODO in moneyController.py)
    connect then close database in every funtion
        --> decorator
"""

class Database():
    def __init__(self, type='', name='', schema='', debug=False):
        self.database= SQLlite_DB(name=name, schema=schema, debug=debug)
        self.name = name
        self.fieldnames = None
        self.table = ''
        self.id = -1

    def connect(self):
        self.database.connect()
    def close(self):
        self.database.close()
    def rollback(self):
        self.database.rollback()

    def query(self, sql, args = None):
        return self.database.query(sql, args)

    def insert(self, table, cols, args):
        if not table:
            table = self.table
        if not cols:
            cols = self.fieldnames
        self.database.insert(self.table, ', '.join(self.fieldnames), args)

    def fetchone(self):
        return self.database.fetchone()

    def fetchall(self):
        return self.database.fetchall()    

    def createTable(self, schema):
        self.database.createTable(schema)
    def dropTable(self, table):
        self.database.dropTable(table)
    def emptyTable(self, table):
        self.database.emptyTable(table)
    def getAllTables(self):
        results = self.database.getAllTables()
        print 'all the tables in the database', results
        #return [result[0] for result in results]
        return results

    def getColumnsSQL(self):
        return 'id, ' + ', '.join(self.fieldnames)

    def getColumns(self, table=''):
        if not table:
            table = self.table
        return self.database.getColumns(table)

    def setInsertColumns(self, table=''):
        if not table:
            table = self.table
        print 'querying all table columns in', self.table
        self.fieldnames = self.database.getInsertColumns(table)
        print 'columns from', self.table, '(without id column):', self.fieldnames    
    def initialize(self, table):
        self.table = table
        self.setInsertColumns()
