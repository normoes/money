from utils.database import Database
import utils.fileChecker as filechecker
from utils.logIt import logIt

import os
import datetime
import fillFromFile as fromCSV

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

    def initialize_table(self):
        print 'selected combobox teblae index:', self.view.dbTables.current()
        #self.setTable(self.view.dbTables.cget('values')[self.view.dbTables.current()])
        #self.db.setInsertColumns()
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
    def populate(self):
        print '===POPULATE==='
        self.view.clearCategories()
        if self.view.dbTables.cget('values')[self.view.dbTables.current()].lower().startswith('cash'):
            self.view.addToCategories('only date and value possible')
        else:
            sql = 'SELECT distinct(category) FROM '+self.db.table+' ORDER BY category COLLATE NOCASE ASC'
            self.db.query(sql)
            rows = self.db.fetchall()
            if rows:
                for row in rows:
                    self.view.addToCategories(row)
    def showEntries(self):
        print '===SHOW ENTRIES==='
        self.view.clearEntries()
        print 'colums from selected table: ', self.db.fieldnames
        sql = 'SELECT '+ self.db.getColumnsSQL() + ' FROM '+self.db.table+' ORDER BY id DESC LIMIT 100'
        # +self.db.fieldnames[0] +
        self.db.query(sql)
        rows = self.db.fetchall()
        if rows:
            for row in rows:
                print 'added to listbox:', row
                self.view.addToEntries(row)

    def populateTablesCombobox(self):
        self.view.dbTables['values'] = self.db.getAllTables()
        print 'all the tables in the combobox:', self.view.dbTables.cget('values')
        # init with firs table in list
        self.view.dbTables.set(self.view.dbTables.cget('values')[0])
    def getDbName(self):
        return os.path.basename(os.path.abspath(self.db.name))
    def setTable(self, table):
        self.db.table = table
    def insertIntoDb(self, args):
        self.view.lastEntry.set(args)
        self.db.insert(table='', cols='', args=args)
        self.showEntries()
    def tableSelect(self, table):
        if table == 'expenditures':
            self.view.initialize_csv(csvFile=self.view.csvFileTARGO)
        elif table == 'cash':
            self.view.initialize_csv(csvFile=self.view.csvFileCASH)
        self.initialize_table()

    def fillFromCSV(self, path):
        if self.filechecker.exists(path):
            print path, 'exists'
            fromCSV.populate(path, self.db)
            self.showEntries()
