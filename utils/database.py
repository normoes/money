from utils.sqlite3_db import SQLlite_DB

class Database():
    def __init__(self, type='', name='', schema='', debug=False):
        self.db= SQLlite_DB(name=name, schema=schema, debug=debug)
        self.name = name
        self.fieldnames = None
        self.table = ''
        self.id = -1

    def query(self, sql, args = None):
        self.db.query(sql, args)

    def insert(self, table, cols, args):
        if not table:
            table = self.table
        if not cols:
            cols = self.fieldnames
        self.db.insert(self.table, ', '.join(self.fieldnames), args)

    def fetchone(self):
        return self.db.fetchone()

    def fetchall(self):
        return self.db.fetchall()

    def close(self):
        self.db.close()

    def createTable(self, schema):
        self.db.createTable(schema)
    def dropTable(self, table):
        self.db.dropTable(table)
    def emptyTable(self, table):
        self.db.emptyTable(table)
    def getAllTables(self):
        results = self.db.getAllTables()
        print 'all the tables in the database', results
        #return [result[0] for result in results]
        return results

    def getColumnsSQL(self):
        return 'id, ' + ', '.join(self.fieldnames)

    def getColumns(self, table=''):
        if not table:
            table = self.table
        return self.db.getColumns(table)

    def setInsertColumns(self, table=''):
        if not table:
            table = self.table
        print 'querying all table columns:'
        self.fieldnames = self.db.getInsertColumns(table)
        print 'columns from', self.table, '(without id column):', self.fieldnames

    def initialize(self, table):
        self.table = table
        self.setInsertColumns()
