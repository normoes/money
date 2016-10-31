import os
import datetime
from utils.database import Database
from utils.inputClient import getCsvReader, checkDate

"""
functions in sqlite
    http://pythoncentral.io/advanced-sqlite-usage-in-python/

uupdate delete insertmany
rollback any change since last commit
    db.rollback()

"""
    
def populate(filename, database=None):
    if database: 
        csvReader, fh = getCsvReader(filename)
        try:
            args= list()                       
            for row in csvReader:
                ddate = checkDate(row['created'].strip())                
                args.append((ddate, row['value'].strip(), row['category'].strip(), row['description'].strip()))
            if len(args) > 0:                
                database.insert(table='expenditures',cols='created, value, category, description', args=args)               
        finally:
            if fh:
                fh.close()