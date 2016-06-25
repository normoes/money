import csv
import os
import datetime
#import utils.fileChecker as filechecker

from utils.MoneyExceptions import *
    
def checkDate_Deco(func):
    def new_func(value):
        date_str = value.split('-')
        error = ''
        ddate, error = func(date_str)
        if not ddate:
            raise NoValidDateException(str(error) + ' / date value: ' + repr(value))
        #assert(not ddate is None), str(error) + ' / date value: ' + repr(value)
        return ddate
    return new_func

## don't forget to close the file, when done 
def getCsvReader(filePath, debug=False):   
    if os.path.exists(filePath) and os.path.isfile(filePath):
        fh = open(filePath, 'rb')
        fieldnames = list()
        header = fh.readline()  
        try:          
            if header.rstrip():
                fieldnames.extend(header.rstrip().split(';'))
        except Exception as e:
            print e
        if debug:
            print fieldnames
        return csv.DictReader(fh, fieldnames, delimiter=";"), fh
    return None, None    
    
@checkDate_Deco    
def checkDate(value):   
    """
    format: 2016-12-28 (year, month, day)
    format: 2016-12 (year, month, day=01)
    format: 12 (year=current, month, day=01)
    """
    error = ''    
    
    year = datetime.datetime.today().strftime('%Y')
    month = ''
    day = '01'
    if len(value) == 1: # only month given
        month = value[0]
    elif len(value) >= 2 and len(value) <= 3:
        year = value[0]
        month = value[1]
        if len(value) == 3:
            day = value[2]
    if len(month) == 1:
        ''.join(['0', month])
    if len(day) == 1:
        ''.join(['0', day])
    try:
        return datetime.date(int(year), int(month), int(day)), error
    except ValueError as e:
        error = e       
    return None, error
    
def checkCategory(value):
    assert(len(value) > 0), 'no category selected'
    return value
def checkDescription(value):
    assert(len(value) > 0), 'no description selected'
    return value    
    
def checkValue(value):
    import re
    p = re.compile(',')
    value = p.sub('.',value)
    if (len(value) == 0) or (value =='-'): 
        raise NotEmptyException('value musn\'t be empty ' + repr(value))
    if value.count('-') > 1:
        raise NumberOfMinusException('too many \'-\' in money value ' + repr(value))
    if value.count('.') > 1:
        raise NumberOfDotsException('too many \'.\' in money value ' + repr(value))
    if value.count('.')==1:
        if len(value.split('.')[1]) > 2:
            raise TooManyDigtsAfterDotException('too many digits after dot ' + repr(value))
    p = re.compile('[-+]?[0-9]*\.?[0-9]*')
    result = p.findall(value)
    assert(len(result)==2), 'check money format: ' + repr(value)
    return float(result[0])
    
def example_getCsvReader(filename, debug=False):
    csvReader, fh = getCsvReader(filename, debug=debug)
    try:    
        if csvReader:             
            for row in csvReader:
                if debug:
                    print row
                try:
                    ddate = checkDate(row['created'])
                    value = checkValue(row['value'])
                    category = checkCategory(row['category'])
                    description = checkCategory(row['description'])
                    yield (ddate, value, category, description)
                except AssertionError as e:
                    print e
    finally:
        if fh:
            fh.close()
            
def test_csv(filename, debug=False):
    example_getCsvReader(filename=filename, debug=debug)

## don't forget to close the file, when done 
def createCsv(filename, fieldnames):   
    fh = None
    print 'creating csv'
    print filename
    try:
        #filecheck = filechecker.fileChecker()        
        fh = open(filename, 'ab')
        
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=";")
        print writer
        print fieldnames
        print 'returning csv'
        return writer, fh
    except:
        return None, None
        
def example_createCsv(filename, fieldnames):    
    writer, fh = createCsv(filename=filename, fieldnames=fieldnames)    
    try:                
        value = -1.23
        writer.writerow({'created': datetime.datetime.today().strftime('%Y-%m-%d'), 'value': value, 'category':'shopping', 'description': 'Hausschuhe'})  
        value = -45.312
        writer.writerow({'created': '2016-2-neu', 'value': value, 'category':'shopping', 'description': 'Hausschuhe'})  
        value = -45.312
        writer.writerow({'created': '2016-2-32', 'value': value, 'category':'shopping', 'description': 'Hausschuhe'}) 
        value = -45.312
        writer.writerow({'created': '2016-0-12', 'value': value, 'category':'shopping', 'description': 'Hausschuhe'}) 
    finally:
        if fh:
            fh.close()
        
if __name__ == '__main__':
    fieldnames = ['created','value','category', 'description']    
    filename = 'money_.txt'
    # write csv file
    example_createCsv(filename=filename,fieldnames=fieldnames)
    # check csv file
    test_csv(filename=filename, debug=True)

    
