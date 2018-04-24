#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import csv
import os
import datetime
import utils.file_checker as file_checker
import logging

logger = logging.getLogger(__name__)


def check_date_deco(func):
    """decorator function for date checking functions

    """
    def new_func(value):
        date_str = value.split('-')
        error = ''
        ddate, error = func(date_str)
        if not ddate:
            raise ValueError(str(error) + ' / date value: ' + repr(value))
        return ddate
    return new_func


def get_csv_reader(filePath, debug=False):  # don't forget to close the file, when done

    if not os.path.isfile(filePath):
        raise ValueError('path not found:{0}'.format(filePath))
    fh = open(filePath, 'r', encoding='utf-8')
    fieldnames = list()
    # from io import BytesIO, StringIO
    header = fh.readline()
    try:
        logger.debug(header.rstrip())
        if header.rstrip():
            fieldnames.extend(header.rstrip().split(';'))
    except Exception:
        logger.exception('getting header from csv')
    if debug:
        logger.debug(fieldnames)
    return csv.DictReader(fh, fieldnames, delimiter=";"), fh


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
    if len(value) == 1:  # only month given
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
    value = p.sub('.', value)
    if (len(value) == 0) or (value == '-'):
        raise ValueError('value musn\'t be empty ' + repr(value))
    if value.count('-') > 1:
        raise ValueError('too many \'-\' in money value ' + repr(value))
    if value.count('.') > 1:
        raise ValueError('too many \'.\' in money value ' + repr(value))
    if value.count('.') == 1:
        if len(value.split('.')[1]) > 2:
            raise ValueError('too many digits after dot ' + repr(value))
    p = re.compile('[-+]?[0-9]*\.?[0-9]*')
    result = p.findall(value)
    assert(len(result) == 2), 'check money format: ' + repr(value)
    return float(result[0])


def example_get_csv_reader(filename='', debug=False):
    if debug:
        logger.debug(filename, debug)
    reader, fh = get_csv_reader(filename, debug=debug)
    print("test reader created")
    try:
        if reader:
            for row in reader:
                if debug:
                    logger.debug(row)
                try:
                    ddate = check_date(row['created'])
                    value = check_value(row['value'])
                    category = check_category(row['category'])
                    description = check_description(row['description'])
                    yield (ddate, value, category, description)
                except AssertionError:
                    logger.exception('validating entry')
                except ValueError:
                    logger.exception('Exception')
    finally:
        if fh:
            fh.close()
    print("done!!")


def test_csv(filename, debug=False):
    print(filename)
    for item in example_get_csv_reader(filename=filename, debug=debug):
        print(item)
    print("done")


def create_csv(filename, fieldnames):  # don't forget to close the file, when done
    try:
        fh = open(filename, 'ab')

        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=";")
        fc = file_checker.fileChecker()
        if fc.isEmpty(filename):
            logger.debug('writing header')
            writer.writeheader()
        logger.debug(fieldnames)
        return writer, fh
    except Exception:
        logger.exception('Exception')
    return None, None


def example_create_csv(filename, fieldnames):
    writer, fh = create_csv(filename=filename, fieldnames=fieldnames)
    try:
        value = -1.23
        writer.writerow({'created': datetime.datetime.today().strftime('%Y-%m-%d'), 'value': value, 'category': 'shopping', 'description': 'Hausschuhe'})
        value = -45.312
        writer.writerow({'created': '2016-2-neu', 'value': value, 'category': 'shopping', 'description': 'Hausschuhe'})
        value = -45.312
        writer.writerow({'created': '2016-2-32', 'value': value, 'category': 'shopping', 'description': 'Hausschuhe'})
        value = -45.312
        writer.writerow({'created': '2016-0-12', 'value': value, 'category': 'shopping', 'description': 'Hausschuhe'})
    finally:
        if fh:
            fh.close()


if __name__ == '__main__':
    FIELDNAMES = ['created', 'value', 'category', 'description']
    FILENAME = 'money_test.txt'
    # write csv file
    example_create_csv(filename=FILENAME, fieldnames=FIELDNAMES)
    # check csv file
    test_csv(filename=FILENAME, debug=True)
