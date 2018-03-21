#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""

This represents the cotroller of the money program.

Here, the database connections are handled and
data is written back into the gui components.
"""

import logging
import os
import fill_from_file as from_csv
from logging.handlers import RotatingFileHandler

from utils.database import Database
import utils.file_checker as fc
from utils.dbConnect_deco import dbConnectAndClose
from utils.ExceptionsDeco import printException


class MoneyController(object):
    """
    The MoneyController() handles database connections/calls and
    writes data back to the GUI.
    """
    def __init__(self, database_name='money.db', path='', debug=False):
        # self.view = view
        self.database = None
        self.debug = debug

        self.database_name = database_name
        self.path = os.path.abspath(os.path.dirname(path))

        self.logger = logging.getLogger('money controller')
        self.logger.setLevel(logging.DEBUG)

        logname = os.path.join(self.path, ('money.log'))
        file_handler = RotatingFileHandler(logname, maxBytes=1000000, backupCount=2)
        file_handler.setLevel(logging.DEBUG)
        # console logger with higher logging level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # self.initialize_db(self.database_name)
        self.filechecker = fc.fileChecker(self.logger)

    @printException
    @dbConnectAndClose
    def initialize_table(self, table=''):
        """
        ===initialize_table(self)===
        The database is initialised by means of selected table (GUI).
        Possible categories are read from the database.
        Get and show the last 100 entries.
        """
        self.logger.debug(table)
        self.database.initialize(table)
        # if self.view:
        #     # print 'selected combobox table index:', self.view.db_tables.current()
        #     # print 'TODOOO:', self.view.db_tables.cget('values')[self.view.db_tables.current()]
        #     # self.database.initialize(self.view.db_tables.cget('values')[self.view.db_tables.current()])
        #     # self.database.initialize(table)
        #     self.view.database_path_str.set(os.path.basename(self.database_name) + ' ' + self.database.table)
        #     print "databse path: ", self.view.database_path_str.get()
        #
        #     self.populate_categories()
        #     self.show_entries()

    def initialize_db(self, database_name):
        # print"===initialize db==="
        if not len(database_name) == 0:
            self.database = Database(name=database_name, debug=True)
            self.database.path = self.path
            # print 'TOCHECK: abs path on start'
            # self.populate_tables_combobox()
            # if self.view:
            #     tablename = self.view.db_tables.cget('values')[self.view.db_tables.current()]
            # else:
            # tablename = 'expenditures'
            #
            # self.initialize_table(table=tablename)

    @printException
    @dbConnectAndClose
    def query(self, sql):
        self.database.query(sql)
        return self.database.fetchall()

    # initialize with data from file
    @printException
    @dbConnectAndClose
    def get_all_categories(self):
        sql = 'SELECT distinct(category) FROM ' + self.database.table + ' ORDER BY category COLLATE NOCASE ASC'
        self.database.query(sql)
        return self.database.fetchall()
    # def populate_categories(self):
    #     print '===populate_categories(self)==='
    #     if self.view:
    #         self.view.clear_categories()
    #         sql = 'SELECT distinct(category) FROM ' + self.database.table + ' ORDER BY category COLLATE NOCASE ASC'
    #         self.database.query(sql)
    #         rows = self.database.fetchall()
    #         if rows:
    #             for row in rows:
    #                 self.view.add_to_categories(row)

    @printException
    @dbConnectAndClose
    def get_latest_entries(self):
        # print 'colums from selected table: ', self.database.fieldnames
        sql = 'SELECT ' + self.database.getColumnsSQL() + ' FROM ' + self.database.table + ' ORDER BY id DESC LIMIT 100'
        # self.database.query(sql)
        return self.database.fetchall()

    @printException
    @dbConnectAndClose
    def get_all_tables(self):
        return self.database.getAllTables()

    @printException
    @dbConnectAndClose
    def get_all_from(self, table_name=''):
        """
        sort by created
        """
        # value, created, category, description
        columns = self.database.get_columns_without_id_sql(table_name)
        sql = 'SELECT {0} FROM {1} ORDER BY created ASC'.format(columns, table_name)
        return self.database.query(sql).fetchall()

    @printException
    @dbConnectAndClose
    def sum_values_for_categories_in(self, table_name, categories):
        columns = 'sum(value)'
        args_str = tuple('?') * len(categories)
        sql = 'SELECT {0} FROM {1} WHERE category in ({2})'.format(columns, table_name, ','.join(args_str))
        return self.database.query(sql, categories).fetchone()[0]

    @printException
    @dbConnectAndClose
    def insert_into_db(self, args):
        self.database.insert(table='', cols='', args=args)

    @printException
    @dbConnectAndClose
    def fill_from_csv(self, path):
        if self.filechecker.exists(path):
            # print path, 'exists'
            from_csv.populate(path, self.database)


if __name__ == '__main__':
    import sys
    logging.debug(sys.argv)
    if len(sys.argv) > 1:
        db = MoneyController(database_name='money.db', path=sys.argv[0])
        logging.debug(db.database)
        db.initialize_db(database_name=db.database_name)
        logging.debug(db.database)
        result = db.query(sys.argv[1])
        if result:
            for l in result:
                print(l)
        else:
            logging.error('query returned nothing')
    else:
        logging.error('provide an sql string')
        raise SystemExit('provide an sql string')
