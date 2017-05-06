#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""

This represents the cotroller of the money program.

Here, the database connections are handled and
data is written back into the gui components.
"""

import os
import datetime
import logging

import fill_from_file as from_csv

from utils.database import Database
import utils.file_checker as fc
from utils.dbConnect_deco import dbConnectAndClose
from utils.ExceptionsDeco import printException

class MoneyController(object):
    """
    The MoneyController() handles database connections/calls and
    writes data back to the GUI.
    """
    def __init__(self, view, database_name='money.db', debug=False):
        self.view = view
        self.database = None
        self.debug = debug
        # print '__name__:', __name__
        # print '__file__:', __file__
        # self.logger = logIt(path = os.path.dirname(os.path.abspath(databaseName)), filename='logger'+datetime.datetime.today().strftime('%Y_%m_%d')+'.txt', debug=True)
        # console logger
        self.logger = logging.getLogger('money controller')
        self.logger.setLevel(logging.DEBUG)
        # file logger
        logname = 'money_'+datetime.datetime.today().strftime('%Y_%m')+'.log'
        file_handler = logging.FileHandler(logname)
        file_handler.setLevel(logging.DEBUG)
        # console logger with higher logging level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.database_name = database_name
        self.initialize_db(self.database_name)
        self.filechecker = fc.fileChecker(self.logger)
    @printException
    @dbConnectAndClose
    def initialize_table(self):
        """
        ===initialize_table(self)===
        The database is initialised by means of selected table (GUI).
        Possible categories are read from the database.
        Get and show the last 100 entries.
        """
        print 'selected combobox table index:', self.view.db_tables.current()
        print 'TODOOO:', self.view.db_tables.cget('values')[self.view.db_tables.current()]
        self.database.initialize(self.view.db_tables.cget('values')[self.view.db_tables.current()])
        self.view.database_path_str.set(os.path.basename(self.database.name)+' '+self.database.table)
        print self.view.database_path_str.get()

        self.populate_categories()
        self.show_entries()

    def initialize_db(self, database_name):
        if not len(database_name) == 0:
            self.database = Database(name=database_name, debug=True)
            self.populate_tables_combobox()
            self.initialize_table()

    # initialize with data from file
    @printException
    @dbConnectAndClose
    def populate_categories(self):
        print '===populate_categories(self)==='
        self.view.clear_categories()
        sql = 'SELECT distinct(category) FROM '+self.database.table+' ORDER BY category COLLATE NOCASE ASC'
        self.database.query(sql)
        rows = self.database.fetchall()
        if rows:
            for row in rows:
                self.view.add_to_categories(row)
    @printException
    @dbConnectAndClose
    def show_entries(self):
        print '===SHOW ENTRIES==='
        self.view.clear_entries()
        print 'colums from selected table: ', self.database.fieldnames
        sql = 'SELECT '+ self.database.getColumnsSQL() + ' FROM '+self.database.table+' ORDER BY id DESC LIMIT 100'
        self.database.query(sql)
        rows = self.database.fetchall()
        if rows:
            for row in rows:
                #print 'added to listbox:', row
                self.view.add_to_entries(row)
    @printException
    @dbConnectAndClose
    def populate_tables_combobox(self):
        self.view.db_tables['values'] = self.database.getAllTables()
        print 'all the tables in the combobox:', self.view.db_tables.cget('values')
        # init with firs table in list
        self.view.db_tables.set(self.view.db_tables.cget('values')[0])
        print 'done populating table comboboxes'
    # def get_db_name(self):
    #     return os.path.basename(os.path.abspath(self.database.name))
    # def set_table(self, table):
    #     self.database.table = table
    @printException
    @dbConnectAndClose
    def insert_into_db(self, args):
        self.view.last_entry.set(args)
        self.database.insert(table='', cols='', args=args)
        self.show_entries()
    def table_select(self, table):
        if table == 'expenditures':
            self.view.initialize_csv(csv_file=self.view.csv_file_targo)
        elif table == 'cash2':
            self.view.initialize_csv(csv_file=self.view.csv_file_cash)
        self.initialize_table()
    @printException
    @dbConnectAndClose
    def fill_from_csv(self, path):
        if self.filechecker.exists(path):
            print path, 'exists'
            from_csv.populate(path, self.database)
            self.show_entries()
