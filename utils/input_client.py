#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import csv
import os
import datetime
import file_checker

def check_date_deco(func):
    """decorator function for date checking functions

    """
    def new_func(value):
        date_str = value.split('-')
        error = ''
        ddate, error = func(date_str)
        if not ddate:
            raise ValueError(str(error) + ' / date value: ' + repr(value))
        #assert(not ddate is None), str(error) + ' / date value: ' + repr(value)
        return ddate
    return new_func

## don't forget to close the file, when done
def get_csv_reader(filePath, debug=False):
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

@check_date_deco
def check_date(value):
    """ function that checks a given date string
    format: 2016-12-28 (year, month, day)
    format: 2016-12 (year, month, day=01)
    format: 12 (year=current, month, day=01)

    >>> check_date

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

def check_category(value):
    assert(len(value) > 0), 'no category selected'
    return value
def check_description(value):
    assert(len(value) > 0), 'no description selected'
    return value

def check_value(value):
    import re
    p = re.compile(',')
    value = p.sub('.',value)
    if (len(value) == 0) or (value =='-'):
        raise ValueError('value musn\'t be empty ' + repr(value))
    if value.count('-') > 1:
        raise ValueError('too many \'-\' in money value ' + repr(value))
    if value.count('.') > 1:
        raise ValueError('too many \'.\' in money value ' + repr(value))
    if value.count('.')==1:
        if len(value.split('.')[1]) > 2:
            raise ValueError('too many digits after dot ' + repr(value))
    p = re.compile('[-+]?[0-9]*\.?[0-9]*')
    result = p.findall(value)
    assert(len(result)==2), 'check money format: ' + repr(value)
    return float(result[0])

def example_get_csv_reader(filename='', debug=False):
    print "n way"
    print "yipiihh"
    print filename, debug
    reader, fh = get_csv_reader(filename, debug=debug)
    print "test reader created"
    try:
        if reader:
            for row in reader:
                if debug:
                    print row
                try:
                    ddate = check_date(row['created'])
                    value = check_value(row['value'])
                    category = check_category(row['category'])
                    description = check_description(row['description'])
                    yield (ddate, value, category, description)
                except AssertionError as e:
                    print e
                except ValueError as ve:
                    print ve
    finally:
        if fh:
            fh.close()
    print "done!!"

def test_csv(filename, debug=False):
    print filename
    for item in example_get_csv_reader(filename=filename, debug=debug):
        print item
    print "done"

## don't forget to close the file, when done
def create_csv(filename, fieldnames):
    try:
        #filecheck = filechecker.fileChecker()
        fh = open(filename, 'ab')

        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=";")
        #print writer
        fc = file_checker.fileChecker()
        if fc.isEmpty(filename):
            print 'writing header'
            writer.writeheader()
        print fieldnames
        #print 'returning csv'
        return writer, fh
    except Exception as e:
        print e
    return None, None


def example_create_csv(filename, fieldnames):
    writer, fh = create_csv(filename=filename, fieldnames=fieldnames)
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
    filename = 'money_test.txt'
    # write csv file
    example_create_csv(filename=filename,fieldnames=fieldnames)
    # check csv file
    test_csv(filename=filename, debug=True)
