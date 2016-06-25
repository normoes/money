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
        
if __name__ == '__main__':
    #print datetime.date.today()
    #my_birthday = datetime.date(1985, 8, 26)
    #print type(my_birthday)
    #print my_birthday
    #import time
    #print datetime.datetime.now() #.strftime('%Y%m%d')
    #print datetime.datetime.fromtimestamp(time.time())
    #print datetime.datetime.utcnow()
    #print datetime.datetime.utcfromtimestamp(time.time())
    #now = datetime.datetime.utcnow()
    #print now.ctime()
    #print now.isoformat()
    #print now.strftime('%Y_%m_%d_%H-%M')
   
    databaseName = 'money.db'
    
    database = Database(name=databaseName, debug=True)
    schema = ("CREATE TABLE cash"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"                      
                      "created DATE NOT NULL,"
                      "value REAL NOT NULL)")
                      #"category TEXT,"
                      #"description TEXT NOT NULL)")
    
    database.createTable(schema)
    #filename = 'money_2016_01_21_10_43_54.txt'
    #populate(database=database, filename=filename)
    
    #sql = 'SELECT * FROM targo'
    #database.query(sql)
    #rows = database.fetchall()
    #if not rows is None:
    #    for row in rows:
    #        print row
    
    """
    sql = 'SELECT * FROM account'
    database.query(sql)
    rows = database.fetchall()
    apr = None
    #if rows is not None:
    #    for row in rows:
    #        print row[2]
    #        print type(row[2])    
    sql = ("INSERT INTO account (created, value, category, description)"
            "values (?,?,?,?)")    
    #args = ('Festo', datetime.datetime.now().strftime('%Y%m%d'), 4303.68)
    args = [(dtoday, 4303.68, 'shopping', 'Festo'), (dtoday, -4303.68, 'shopping1', 'Festo1')]
    database.insert(table='account',cols='created, value, category, description', args=args)
    """
