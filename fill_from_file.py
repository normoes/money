#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import logging
from utils import database
from utils.input_client import get_csv_reader, check_date

logging.basicConfig(level=logging.DEBUG)


def populate(filename, database=None):
    assert(database is not None), 'no database provided'
    reader, fh = get_csv_reader(filename)  # TODO context manager that closes fh
    logging.error(reader)
    try:
        args = list()
        g = database.insert_co(table='expenditures')
        g.next()
        for row in reader:
            ddate = check_date(row['created'].strip())
            args.append((ddate, row['value'].strip(), row['category'].strip(), row['description'].strip()))
        if len(args) > 0:
            g.send(args)
            # database.insert(table='expenditures', cols='created, value, category, description', args=args)
    finally:
        if fh:
            fh.close()


if __name__ == '__main__':
    import sys
    logging.debug(sys.argv)
    if len(sys.argv) > 1:
        import os
        if os.path.exists(sys.argv[1]):
            db = database.Database(name=sys.argv[1], debug=True)
            populate(filename='fill_from_csv.template', database=db)
        else:
            raise SystemExit('database not found')
    else:
        raise SystemExit('closing')
