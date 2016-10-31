from utils.database import Database
import utils.fileChecker as filechecker
from utils.logIt import logIt

import os
import datetime
import fillFromFile as fromCSV
from utils.dbConnect_deco import dbConnectAndClose
from utils.ExceptionsDeco import printException



"""

TODO (see database.py, do it in there)
    open + close database afterevery transaction
    --> can be used with server application
    --> sqlitebrowser, server application and input_gui can besed at the sametime
        --> database is not locked then
    --> ATTENTION: fetchone(), fetchall() called after execute (no db.close in between)

"""


class moneyController():

    def __init__(self, view,  databaseName = 'money.db', debug=False):
        self.view = view
        self.db = None
        print __name__
        print __file__
        self.logger = logIt(path = os.path.dirname(os.path.abspath(databaseName)), filename='logger'+datetime.datetime.today().strftime('%Y_%m_%d')+'.txt', debug=True)
        self.databaseName = databaseName
        self.initialize_db(self.databaseName)
        self.filechecker = filechecker.fileChecker(self.logger)
    @printException
    @dbConnectAndClose
    def initialize_table(self):
        print 'selected combobox table index:', self.view.dbTables.current()
        print 'TODOOO:', self.view.dbTables.cget('values')[self.view.dbTables.current()]
        self.db.initialize(self.view.dbTables.cget('values')[self.view.dbTables.current()])
        self.view.databasePath_str.set(os.path.basename(self.db.name)+' '+self.db.table)

        self.populate()
        self.showEntries()

    def initialize_db(self, databaseName):
        if not len(databaseName) == 0:
            self.db = Database(name=databaseName, debug=True)
            self.populateTablesCombobox()
            self.initialize_table()

    # initialize with data from file
    @printException
    @dbConnectAndClose
    def populate(self):
        print '===POPULATE==='
        self.view.clearCategories()
        sql = 'SELECT distinct(category) FROM '+self.db.table+' ORDER BY category COLLATE NOCASE ASC'
        self.db.query(sql)
        rows = self.db.fetchall()
        if rows:
            for row in rows:
                self.view.addToCategories(row)
    @printException
    @dbConnectAndClose
    def showEntries(self):
        print '===SHOW ENTRIES==='
        self.view.clearEntries()
        print 'colums from selected table: ', self.db.fieldnames
        sql = 'SELECT '+ self.db.getColumnsSQL() + ' FROM '+self.db.table+' ORDER BY id DESC LIMIT 100'
        self.db.query(sql)
        rows = self.db.fetchall()
        if rows:
            for row in rows:
                #print 'added to listbox:', row
                self.view.addToEntries(row)
    @printException
    @dbConnectAndClose
    def populateTablesCombobox(self):
        self.view.dbTables['values'] = self.db.getAllTables()
        print 'all the tables in the combobox:', self.view.dbTables.cget('values')
        # init with firs table in list
        self.view.dbTables.set(self.view.dbTables.cget('values')[0])
        print 'done populating table comboboxes'
    def getDbName(self):
        return os.path.basename(os.path.abspath(self.db.name))
    def setTable(self, table):
        self.db.table = table
    @printException
    @dbConnectAndClose
    def insertIntoDb(self, args):
        self.view.lastEntry.set(args)
        self.db.insert(table='', cols='', args=args)
        self.showEntries()
    def tableSelect(self, table):
        if table == 'expenditures':
            self.view.initialize_csv(csvFile=self.view.csvFileTARGO)
        elif table == 'cash2':
            self.view.initialize_csv(csvFile=self.view.csvFileCASH)
        self.initialize_table()
    @printException
    @dbConnectAndClose
    def fillFromCSV(self, path):
        if self.filechecker.exists(path):
            print path, 'exists'
            fromCSV.populate(path, self.db)
            self.showEntries()
