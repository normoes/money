#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import logging
from utils import database
from utils.input_client import get_csv_reader, check_date

logging.basicConfig(level=logging.DEBUG)


def populate(filename, database=None):
    assert(database is not None), 'no database provided'
    reader, fh = get_csv_reader(filename)  # TODO context manager that closes fh
    logging.error('reader: {0}'.format(reader))
    try:
        args = list()
        g = database.insert_co(table='expenditures')
        try:
            logging.debug(g)
            next(g)
            for row in reader:
                logging.debug(row)
                ddate = check_date(row['created'].strip())
                args.append((ddate, row['value'].strip(), row['category'].strip(), row['description'].strip()))
            if len(args) > 0:
                logging.debug('sending data: {}'.format(args))
                g.send(args)
        finally:
            g.close()
    finally:
        if fh:
            fh.close()


if __name__ == '__main__':
    import sys
    import os
    logging.debug(sys.argv)
    _path, _ = os.path.split(sys.argv[0])
    _path = os.path.abspath(_path)
    if len(sys.argv) > 1:
        db = database.Database(name=sys.argv[1], debug=True)
        db.connect()
        try:
            populate(filename=os.path.join(_path, 'fill_from_csv.template'), database=db)
        finally:
            db.close()
    else:
        raise SystemExit('provide a database path')
