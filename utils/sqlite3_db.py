import sqlite3
import logging
from utils.ExceptionsDeco import printException

logger = logging.getLogger(__name__)


class SqliteDb():
    """
    If you're using SQLite version 3.3+ you can easily create a table with:
    .. code-block:: python
            create table if not exists TableName (col1 typ1, ..., colN typN)
    In the same way, you can remove a table only if it exists by using:
    .. code-block:: python
            drop table if exists TableName
    """
    def __init__(self, name='', schema='', debug=False):
        self.name = name
        self.schema = schema
        self.path = ''
        self.dbPath = ''
        self.connection = None
        self.cursor = None
        self.debug = debug

        self.createTable(self.schema)

    @printException
    def rollback(self):
        if self.connection:
            logger.warn('rolling back')
            self.connection.rollback()

    @printException
    def close(self):
        if self.connection:
            logger.debug('closing connection')
            self.connection.close()
            self.connection = None
            self.cursor = None

    @printException
    def connect(self):
        if self.debug:
            logger.debug('connect to database')
        return self.connection is not None

    def init_connection(self):
        if self.debug:
            logger.debug('initialize database connection')
        # connect method:
        # store dates as datetime.date (when datetime.date.today()) --> column type db DATE (2013-04-14)
        # store dates as datetime.datetime (when datetime.now()) --> column type db TIMESTAMP (2013-04-14 16:29:11.666274)
        # --> not as string
        # when column type is DATE but return type shall be DATETIME modify query (when datetime.now())
        # '''SELECT created_at as "colName [timestamp]" FROM example'''
        if not self.dbPath:
            raise ValueError('missing database path')
        self.connection = sqlite3.connect(self.dbPath, detect_types=sqlite3.PARSE_COLNAMES)  # sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
        if not self.connection:
            raise ValueError('no connection established to {0}'.format(self.dbPath))
        self.cursor = self.connection.cursor()

    @printException
    def query(self, sql, args=None):
        return self.execute(sql, args)

    def execute(self, sql, args=None):
        sql = sql.strip()

        if self.debug:
            logger.debug('sql:{0}, args: {1}'.format(repr(sql), repr(args)))
        if args:
            return self.cursor.execute(sql, args)
        else:
            return self.cursor.execute(sql)
        self.commit()

    @printException
    def executeScript(self, script):
        raise NotImplementedError('executeScript')
        # script = '''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
        #    CREATE TABLE accounts(id INTEGER PRIMARY KEY, description TEXT);
        #
        #    INSERT INTO users(name, phone) VALUES ('John', '5557241'),
        #     ('Adam', '5547874'), ('Jack', '5484522');'''
        # c.executescript(script)

    @printException
    def insert(self, table, cols, args):
        #     sql = ('INSERT INTO account (description, date, value) values (?,?,?)')
        args_str = tuple('?') * len(args[0])
        sql = 'INSERT INTO {0}({1}) values ({2})'.format(table.strip(), cols.strip(), ','.join(args_str))
        if self.debug:
            logger.debug(sql, args)
        self.cursor.executemany(sql, args)
        self.commit()

# update and delete
# # Update user with id 1
# newphone = '3113093164'
# userid = 1
# cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',
# (newphone, userid))

# # Delete user with id 2
    # delete_userid = 2
    # cursor.execute('''DELETE FROM users WHERE id = ? ''', (delete_userid,))

    # db.commit()
    @printException
    def fetchone(self):
        return self.cursor.fetchone()

    @printException
    def fetchall(self):
        return self.cursor.fetchall()

    @printException
    def commit(self):
        self.connection.commit()

    @printException
    def getColumns(self, table_name):
        self.query('SELECT * FROM ' + table_name)
        return [description[0] for description in self.cursor.description]

    @printException
    def getInsertColumns(self, table_name):
        """
        gets all the columns and rmeoves the first column 'ID'
        """
        fieldnames = self.getColumns(table_name)
        fieldnames.pop(0)  # remove column 'ID'
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
            self.execute(schema)
            if self.debug:
                logger.debug(table, 'created')

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

    # def _tableExists(self, tableName):
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
    def getAllTables(self):
        """getAllTables

         # using  "SELECT name FROM sqlite_master" or sqlite_sequence??
            sqlite_sequence is created if at least one autoincrement field in table

        that's why:
         in def getAllTables(self):
             # sql = "SELECT name FROM sqlite_sequence"
                 --> does not find renamed table, because not in sqlite_sequence
                 --> tables are in sqlite_sequence if auto incremented primary key is available
                 # sql = "SELECT name FROM sqlite_master where type = 'table'"

        getting a specific table:
        # sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';".format(tableName)

        :return list: a list of tables in the database
        :rtype: list
        """
        sql = "SELECT name FROM sqlite_master where type = 'table'"
        # sql = "SELECT name FROM sqlite_sequence"
        self.execute(sql)
        if self.debug:
            logger.debug('getting all the tables')
        return [result[0] for result in self.fetchall() if not result[0] == 'sqlite_sequence']
