import logging
import os
from utils.sqlite3_db import SqliteDb

logger = logging.getLogger(__name__)


class Database():
    def __init__(self, type='', name='', schema='', debug=False):
        self.database = SqliteDb(name=name, schema=schema, debug=debug)
        self.name = name
        self.path = ''
        self.fieldnames = None
        self.table = ''
        self.id = -1

    def connect(self):
        if not self.database.connect():
            self.database.dbPath = self.get_abs_path(self.name)
            if not os.path.exists(self.database.dbPath):
                raise ValueError('path does not exist:{0}'.format(self.database.dbPath))
            self.database.init_connection()

    def close(self):
        self.database.close()

    def rollback(self):
        self.database.rollback()

    def query(self, sql, args=None):
        return self.database.query(sql, args)

    def insert(self, table, cols, args):
        self.database.insert(self.table, ', '.join(self.fieldnames), args)

    def insert_co(self, table):
        while True:
            args = yield
            logger.debug('insert: {0}'.format(args))
            self.database.insert(table, ', '.join(self.fieldnames), args)

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
        logger.debug('all the tables in the database: {}'.format(results))
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
        logger.debug('querying all table columns in: {}'.format(self.table))
        self.fieldnames = self.database.getInsertColumns(table)
        logger.debug('columns from: {0} without id column): {1}'.format(self.table, self.fieldnames))

    def initialize(self, table):
        self.table = table
        self.setInsertColumns()

    def get_abs_path(self, filename):
        _path, name = os.path.split(filename)
        if not _path:
            _path = self.path
        logger.debug('absolute path: {}'.format(_path))
        # abspath, since _path could be relative
        return os.path.join(os.path.abspath(_path), name)
