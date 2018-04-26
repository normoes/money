#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""

This represents the cotroller of the money program.

Here, the database connections are handled and
data is written back into the gui components.
"""

import argparse
import sys
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
        self.database = None
        self.debug = debug

        self.database_name = database_name
        self.path = path

        self.logger = logging.getLogger('money controller')
        self.logger.setLevel(logging.DEBUG)

        logname = os.path.join(os.path.abspath(os.path.dirname(self.path)), ('money.log'))
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

    def initialize_db(self, database_name):
        # print"===initialize db==="
        if not len(database_name) == 0:
            self.database = Database(name=database_name, debug=True)

    @printException
    @dbConnectAndClose
    def query(self, sql):
        self.database.query(sql)
        return self.database.fetchall()

    # initialize with data from file
    @printException
    @dbConnectAndClose
    def get_all_categories(self, table=''):
        if not table:
            table = self.database.table
        sql = 'SELECT distinct(category) FROM ' + table + ' ORDER BY category COLLATE NOCASE ASC'
        self.database.query(sql)
        return self.database.fetchall()

    @printException
    @dbConnectAndClose
    def get_all_tables(self):
        return self.database.getAllTables()

    @printException
    @dbConnectAndClose
    def get_latest_from(self, table):
        # print 'colums from selected table: ', self.database.fieldnames
        # sql = 'SELECT ' + self.database.getColumnsSQL() + ' FROM ' + table + ' ORDER BY id DESC LIMIT 100'
        columns = self.database.getColumnsSQL()
        self.logger.error(columns)
        sql = 'SELECT {0} FROM {1} ORDER BY created DESC LIMIT 25'.format(columns, table)
        self.database.query(sql)
        return self.database.fetchall()

    @printException
    @dbConnectAndClose
    def get_all_from(self, table=''):
        """
        sort by created
        """
        # value, created, category, description
        columns = self.database.get_columns_without_id_sql(table)
        sql = 'SELECT {0} FROM {1} ORDER BY created ASC'.format(columns, table)
        self.database.query(sql)
        return self.database.fetchall()

    @printException
    @dbConnectAndClose
    def sum_values_for_categories_in(self, table, categories):
        columns = 'sum(value)'
        args_str = tuple('?') * len(categories)
        sql = 'SELECT {0} FROM {1} WHERE category in ({2})'.format(columns, table, ','.join(args_str))
        self.database.query(sql, categories)
        return self.database.fetchone()[0]

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

    def validate_input(self, ddate, value, category, description):
        from utils.input_client import check_date, check_value
        from utils.input_client import check_category, check_description

        try:
            ddate = check_date(value=ddate)
            value = check_value(value=value)
            category = check_category(value=category)
            description = check_description(value=description)

            args = [(ddate, value, category, description)]
            return args
        except AssertionError as e:
            self.logger.error(e)
        except ValueError as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.error(e)

        return None


class MyParser(argparse.ArgumentParser):
    def __init__(self, prog):
        super().__init__()

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(prog=os.path.split(__file__)[1])
    parser = MyParser(prog=os.path.split(__file__)[1])
    # gp = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-l', '--list', help='list e.g.categories', action="store_true")
    parser.add_argument('-i', '--insert', help='format: 2018-03-28 -12.34 home some spare parts')
    parser.add_argument('-t', '--table', help='db table to query', required=True)
    parser.add_argument('-db', '--database', help='database to use, money.db?', required=True)
    values = parser.parse_args()

    # logging.debug(sys.argv)
    # logging.debug(values.table)
    # if len(sys.argv) > 1:
    db = MoneyController(database_name=values.database, path=sys.argv[0])
    # logging.debug('name: {0}'.format(db.database))
    db.initialize_db(database_name=db.database_name)
    if values.list:
            result = db.get_all_categories(values.table)
            if result:
                print('output:', '======', sep='\n')
                for category in result:
                    print(category[0])
            else:
                logging.error('query returned nothing')
    elif values.insert:
        db.initialize_table(table=values.table)
        # db.initialize_table(table=values.table)
        ddate, value, category, *description = values.insert.split(' ')
        args = db.validate_input(ddate=ddate, value=value, category=category, description=' '.join(description))
        try:
            db.insert_into_db(args=args)
        except Exception as e:
            db.logger.error(e)
            raise SystemExit(e)
    elif values.table:
        try:
            db.initialize_table(table=values.table)
            # logging.debug(db.database)
            # result = db.query(values.test_sql)
            result = db.get_latest_from(table=values.table)
            if result:
                print('output:', '======', sep='\n')
                for l in result:
                    print(l)
            else:
                logging.error('query returned nothing')
        except Exception as e:
            logging.error(e)
            raise SystemExit(e)
