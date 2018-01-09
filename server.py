#!/usr/bin/env python

"""money server

:Info: No info yet.
:Author: Norman <normo@posteo.de>
:Date: 2017-12-20
:Version: 0.0.1
:Description: This is the money server.
    Here all the requests arrive and are handled.
"""

import os.path
# import sqlite3
import json
from flask import Flask, request, jsonify, make_response
import logging
import os


import utils.logger_factory as logger_factory
from utils.server import configuration
# from utils.database import Database
# from utils.dbConnect_deco import dbConnectAndClose
# from utils.ExceptionsDeco import printException
import money_controller as control

DB_STRING = "money.db"
# DB_STRING = "moneyTest.db"
SUB_FOLDER = 'server'

APP = Flask('money_server')
"""The APP constant represents the actual server."""
DB_CONTROLLER = None

# class Money(object):
#     @cherrypy.expose
#     def index(self):
#         return file(os.path.join(SUB_FOLDER, 'index.html'))


# class MoneyWebService(object):
#     exposed = True

    # @cherrypy.tools.accept(media='text/plain')
    # def GET(self):
    #     with sqlite3.connect(DB_STRING) as c:
    #         # cherrypy.session['ts'] = time.time()
    #         r = c.execute("SELECT value, created, category, description FROM expenditures ORDER BY created DESC")  # WHERE session_id=?", [cherrypy.session.id])
    #         data = r.fetchall()
    #         json_data = list()
    #         for d in data:
    #             json_data.append({'value': d[0], 'created': d[1], 'category': d[2], 'description': d[3]})
    #         return json.dumps(json_data)

    # def POST(self, sql='SELECT value, created, category, description FROM expenditures ORDER BY created DESC'):
    #     print 'sql', sql
    #     with sqlite3.connect(DB_STRING) as c:
    #         # cherrypy.session['ts'] = time.time()
    #         r = c.execute(sql)
    #         data = r.fetchall()
    #         json_data = list()
    #         print 'data', data
    #         for d in data:
    #             json_data.append({'value': d[0], 'created': d[1], 'category': d[2], 'description': d[3]})
    #         return json.dumps(json_data)
    #
    # def PUT(self, another_string):
    #     """
    #     """
    #     pass
    #     # with sqlite3.connect(DB_STRING) as c:
    #     #     cherrypy.session['ts'] = time.time()
    #     #     c.execute("UPDATE user_string SET value=? WHERE session_id=?",
    #     #                [another_string, cherrypy.session.id])
    #
    # def DELETE(self):
    #     """
    #     """
    #     pass
    #     # cherrypy.session.pop('ts', None)
    #     # with sqlite3.connect(DB_STRING) as c:
    #     #     c.execute("DELETE FROM user_string WHERE session_id=?",
    #     #                [cherrypy.session.id])

# class DatabaseController(object):
#     """docstring for DatabaseController."""
#     def __init__(self, name):
#         self.database_name = name
#         self.database = Database(name=self.database_name, debug=True)
#         self.init_db()
#
#     @dbConnectAndClose
#     def init_db(self):
#         self.database.initialize('cash')
#
#     @printException
#     @dbConnectAndClose
#     def get_cash(self):
#         print 'database name', self.database_name
#         # r= c.execute("SELECT value, created, category, description FROM cash ORDER BY created DESC") #WHERE session_id=?", [cherrypy.session.id])
#         r = self.database.query('SELECT value, created, category, description FROM cash ORDER BY created DESC')  # WHERE session_id=?", [cherrypy.session.id])
#         return r.fetchall()


# @printException
# @dbConnectAndClose
@APP.route('/cash', methods=['GET'])
def get_all():
    table_name = 'cash'
    data = DB_CONTROLLER.get_all_from(table_name=table_name)
    json_data = list()
    for d in data:
        json_data.append({'id': d[0], 'created': d[1], 'value': d[2], 'category': d[3], 'description': d[4]})
    return json.dumps(json_data)


@APP.route('/cash/sum', methods=['GET'])
def get_sum():
    table_name = 'cash'
    json_data = list()
    categories = request.args.get('categories')
    if categories:
        categories = request.args.get('categories').split(',')
        data = DB_CONTROLLER.sum_values_for_categories_in(table_name=table_name, categories=categories)
        if data:
            result = round(data, 2)
            json_data.append({'table': table_name, 'categories': categories, 'sum': result})
    return json.dumps(json_data)

#     def POST(self, sql='SELECT value, created, category, description FROM cash ORDER BY created DESC'):
#         print 'sql', sql
#         with sqlite3.connect(DB_STRING) as c:
#             # cherrypy.session['ts'] = time.time()
#             r = c.execute(sql)
#             data = r.fetchall()
#             json_data = list()
#             print 'data', data
#             for d in data:
#                 json_data.append({'value': d[0], 'created': d[1], 'category': d[2], 'description': d[3]})
#             return json.dumps(json_data)
#
#     def PUT(self, another_string):
#         """
#         """
#         pass
#         # with sqlite3.connect(DB_STRING) as c:
#         #     cherrypy.session['ts'] = time.time()
#         #     c.execute("UPDATE user_string SET value=? WHERE session_id=?",
#         #                [another_string, cherrypy.session.id])
#
#     def DELETE(self):
#         """
#         """
#         pass
#         # cherrypy.session.pop('ts', None)
#         # with sqlite3.connect(DB_STRING) as c:
#         #     c.execute("DELETE FROM user_string WHERE session_id=?",
#         #                [cherrypy.session.id])
#
#
# def setup_database():
#     """
#     """
#     pass
#     # Create the `user_string` table in the database
#     # on server startup
#     #
#     # with sqlite3.connect(DB_STRING) as con:
#     #     con.execute("CREATE TABLE user_string (session_id, value)")
#
#
# def cleanup_database():
#     """
#     """
#     pass
#     # Destroy the `user_string` table from the database
#     # on server shutdown.
#     #
#     # with sqlite3.connect(DB_STRING) as con:
#     #     con.execute("DROP TABLE user_string")


def initialize_db(database_name):
    DB_CONTROLLER.initialize_db(database_name=database_name)


if __name__ == '__main__':
    # allow logging.WARN and logging.INFO and logging.DEBUG even before calling APP.run(debug=True, ...)
    APP.debug = True
    # set to logging.INFO
    if APP.debug:
        APP.logger.setLevel(logging.INFO)
    # # add additional loggers to APP
    file_handler = logger_factory.get_file_handler(file_name='money_server.log')
    APP.logger.addHandler(file_handler)

    URL = os.getenv('URL', default='127.0.0.1')
    APP.logger.info('URL used ' + URL)
    PORT = os.getenv('PORT', default='5000')
    APP.logger.info('port used ' + PORT)

    # get additional resources
    project_path = os.path.abspath(__file__)
    APP.logger.info(project_path)
    extra_files = configuration.get_additional_files_to_watch(project_path)

    DB_CONTROLLER = control.MoneyController(database_name=DB_STRING)
    initialize_db(database_name=DB_STRING)

    APP.run(extra_files=extra_files, host=URL, port=int(PORT))
