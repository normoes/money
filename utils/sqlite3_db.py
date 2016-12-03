import sqlite3
import os

from utils.ExceptionsDeco import printException

"""
using  "SELECT name FROM sqlite_master" or sqlite_sequence??
    sqlite_sequence is created if at least one autoincrement field in table

in def getAllTables(self):
    sql = "SELECT name FROM sqlite_sequence"
        --> does not find renamed table, because not in sqlite_sequence
        --> tables are in sqlite_sequence if auto incremented primary key is available
        sql = "SELECT name FROM sqlite_master where type = 'table'"
        #

"""

class SQLlite_DB():
    def __init__(self, name='', schema='', debug=False):
        self.name = name
        self.schema = schema
        self.path = ''
        self.dbPath = ''
        self._setDbPath()
        self.connection = None
        self.cursor = None
        self.debug = debug

        #self.connect()
        self.createTable(self.schema)
    @printException
    def rollback(self):
        if self.connection:
            print 'rolling back'
            self.connection.rollback()
    @printException
    def close(self):
        if self.connection:
            print 'closing connection'            
            self.connection.close()
            self.connection = None
            self.cursor = None
    @printException
    def connect(self):
        print '--> ', self.connection
        if not self.connection:
            print '--> checking db path'
            if not self.dbPath:
                self._setDbPath()

            #connect method:
            #store dates as datetime.date (when datetime.date.today()) --> column type db DATE (2013-04-14)
            #store dates as datetime.datetime (when datetime.now()) --> column type db TIMESTAMP (2013-04-14 16:29:11.666274)
            #--> not as string
            # when column type is DATE but return type shall be DATETIME modify query (when datetime.now())
                # '''SELECT created_at as "colName [timestamp]" FROM example'''
            print '--> db path', self.dbPath
            if self.dbPath:
                print '--> db connection', self.connection
                self.connection = sqlite3.connect(self.dbPath, detect_types=sqlite3.PARSE_COLNAMES) #sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
                print '--> db connection', self.connection
                if self.connection:
                    print '--> db cursor', self.cursor
                    self.cursor = self.connection.cursor()
                    print '--> db cursor', self.cursor
    @printException
    def query(self, sql, args = None):
        return self.execute(sql, args)
    #@printException
    def execute(self, sql, args = None):
        sql = sql.strip()
        #try:
        #if sql:
        if self.debug:
            print 'sql:', repr(sql), 'args:',repr(args)
        if args:
            return self.cursor.execute(sql, args)
        else:
            return self.cursor.execute(sql)
        self.commit()        
        #    return True
        #except sqlite3.OperationalError as e:
        #    raise TableExistsError(e)
        #return False
    @printException
    def executeScript(self, script):
        pass
        #script = '''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
        #    CREATE TABLE accounts(id INTEGER PRIMARY KEY, description TEXT);
        #
        #    INSERT INTO users(name, phone) VALUES ('John', '5557241'),
        #     ('Adam', '5547874'), ('Jack', '5484522');'''
        #c.executescript(script)
    @printException
    def insert(self, table, cols, args):
        """
        sql = ("INSERT INTO account (description, date, value) values (?,?,?)")
        """
        args_str = tuple('?') * len(args[0])
        sql = 'INSERT INTO {0}({1}) values ({2})'.format(table.strip(), cols.strip(), ','.join(args_str))
        print sql, args
        self.cursor.executemany(sql, args)        
        self.commit()        
##update and delete
    ## Update user with id 1
#newphone = '3113093164'
#userid = 1
#cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',
 #(newphone, userid))

## Delete user with id 2
    #delete_userid = 2
    #cursor.execute('''DELETE FROM users WHERE id = ? ''', (delete_userid,))

    #db.commit()
    @printException
    def fetchone(self):
        return self.cursor.fetchone()
    @printException
    def fetchall(self):
        return self.cursor.fetchall()
    @printException
    def commit(self):
        self.connection.commit()

    #def _tableExists(self, tableName):
    #    if tableName:
    #        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';".format(tableName)
    #        print sql
    #        #sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='"+tableName+"';"
    #        if self.query(sql):
    #            if self.fetchone() is not None:
    #                if self.debug:
    #                    print tableName,'exists'
    #                return True
    #    return False

    @printException
    def getColumns(self, tableName):
        self.query('SELECT * FROM '+tableName)
        return [description[0] for description in self.cursor.description]
    @printException
    def getInsertColumns(self, tableName):
        #print '    column names', self.getColumns(tablename)
        fieldnames = self.getColumns(tableName)
        fieldnames.pop(0) # remove column 'ID'
        return fieldnames

    @printException
    def createTable(self, schema):     
        def getTableName(schema):
            schema = schema.strip()
            schemaParts = schema.upper().split()
            if schemaParts[0].strip() == 'CREATE' and schemaParts[1].strip() == 'TABLE':
                if len(schemaParts) > 3:
                    return schemaParts[2].strip().split('(')[0]
            return ''        
        if schema:            
            table = getTableName(schema)
            #try:
            self.execute(schema)
            if self.debug:
                print table,'created'            
    @printException
    def emptyTable(self, table):        
        sql = 'DELETE FROM ' + table
        self.execute(sql)
        sql = "DELETE FROM sqlite_sequence WHERE name ='{0}'".format(table)
        self.execute(sql)

    def dropTable(self, table):
        self.emptyTable(table)
        sql = "DROP TABLE {0}".format(table)
        self.execute(sql)
    @printException
    def getAllTables(self):
        sql = "SELECT name FROM sqlite_master where type = 'table'"
        #sql = "SELECT name FROM sqlite_sequence"
        self.execute(sql)
        print 'getting all the tables'
        return [result[0] for result in self.fetchall() if not result[0] == 'sqlite_sequence']

    def _setDbPath(self):
        if self.name:
            # make absolute paths
            _path, _name = os.path.split(self.name)
            if not _path:
                self.path = os.path.dirname(os.path.abspath(_name)) #os.getcwdu() # unicode
                print self.path
            else:
                self.path = _path
            self.dbPath = os.path.join(self.path, self.name)

    def _checkPaths(self):
        print repr(self.path)
        print repr(self.dbPath)
        if os.path.exists(self.dbPath):
            print 'exists', self.dbPath
        else:
            print 'does not exist', self.dbPath
