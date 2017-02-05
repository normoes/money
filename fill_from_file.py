#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os
import datetime
from utils.database import Database
from utils.input_client import get_csv_reader, check_date

"""
functions in sqlite
    http://pythoncentral.io/advanced-sqlite-usage-in-python/

uupdate delete insertmany
rollback any change since last commit
    db.rollback()

"""

def populate(filename, database=None):
    if database:
        reader, fh = get_csv_reader(filename)
        try:
            args= list()
            for row in reader:
                ddate = check_date(row['created'].strip())
                args.append((ddate, row['value'].strip(), row['category'].strip(), row['description'].strip()))
            if len(args) > 0:
                database.insert(table='expenditures',cols='created, value, category, description', args=args)
        finally:
            if fh:
                fh.close()
