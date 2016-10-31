import os, os.path
#import random
import sqlite3
#import string
import time

import cherrypy
import json

from utils.database import Database
from utils.dbConnect_deco import dbConnectAndClose
from utils.ExceptionsDeco import printException



DB_STRING = "money.db"
#DB_STRING = "moneyTest.db"
SUB_FOLDER = 'server'


db = Database(name=DB_STRING, debug=True)
db.initialize('cash')

class Money(object):
    @cherrypy.expose
    def index(self):
        return file(os.path.join( SUB_FOLDER,'index.html'))

class MoneyWebService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
            with sqlite3.connect(DB_STRING) as c:
                #cherrypy.session['ts'] = time.time()
                r= c.execute("SELECT value, created, category, description FROM expenditures ORDER BY created DESC") #WHERE session_id=?", [cherrypy.session.id])
                data = r.fetchall()
                json_data = list()
                for d  in data:
                    json_data.append({'value':d[0], 'created':d[1], 'category':d[2], 'description':d[3]})
                return json.dumps(json_data)

    def POST(self, sql='SELECT value, created, category, description FROM expenditures ORDER BY created DESC'):
        print 'sql', sql
        with sqlite3.connect(DB_STRING) as c:
            #cherrypy.session['ts'] = time.time()
            r = c.execute(sql)
            data = r.fetchall()
            json_data = list()
            print 'data', data
            for d  in data:
                json_data.append({'value':d[0], 'created':d[1], 'category':d[2], 'description':d[3]})
            return json.dumps(json_data)

    def PUT(self, another_string):
        """
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            c.execute("UPDATE user_string SET value=? WHERE session_id=?",
                       [another_string, cherrypy.session.id])
        """

    def DELETE(self):
        """
        cherrypy.session.pop('ts', None)
        with sqlite3.connect(DB_STRING) as c:
            c.execute("DELETE FROM user_string WHERE session_id=?",
                       [cherrypy.session.id])
        """

class CashWebService(object):
    exposed = True

    def __init__(self, db):
        self.db = db

    @printException
    @dbConnectAndClose
    @cherrypy.tools.accept(media='text/plain')
    def GET(self): # , *args, **kwargs):
        #with sqlite3.connect(DB_STRING) as c:
        ##cherrypy.session['ts'] = time.time()
        print 'database name', self.db.name
        #r= c.execute("SELECT value, created, category, description FROM cash ORDER BY created DESC") #WHERE session_id=?", [cherrypy.session.id])        
        r= self.db.query('SELECT value, created, category, description FROM cash ORDER BY created DESC') #WHERE session_id=?", [cherrypy.session.id])        
        data = r.fetchall()
        print 'executed'
        json_data = list()
        for d  in data:
            json_data.append({'value':d[0], 'created':d[1], 'category':d[2], 'description':d[3]})
        return json.dumps(json_data)
            #r = c.execute("SELECT value, created FROM cash ORDER BY id DESC")
            #data = r.fetchall()
            #print 'DATA', data
            #json_data = list()
            #for d  in data:
            #    json_data.append({'value':d[0], 'created':d[1]})
            #return json.dumps(json_data)
    def POST(self, sql='SELECT value, created, category, description FROM cash ORDER BY created DESC'):
        print 'sql', sql
        with sqlite3.connect(DB_STRING) as c:
            #cherrypy.session['ts'] = time.time()
            r = c.execute(sql)
            data = r.fetchall()
            json_data = list()
            print 'data', data
            for d  in data:
                json_data.append({'value':d[0], 'created':d[1], 'category':d[2], 'description':d[3]})
            return json.dumps(json_data)
    #def POST(self, sql='SELECT value, created FROM cash ORDER BY id DESC'):
    #    print sql
    #    with sqlite3.connect(DB_STRING) as c:
    #        cherrypy.session['ts'] = time.time()
    #        r= c.execute(sql)
    #        data = r.fetchall()
    #        json_data = list()
    #        for d  in data:
    #            json_data.append({'value':d[0], 'created':d[1]})
    #        return json.dumps(json_data)

    def PUT(self, another_string):
        """
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            c.execute("UPDATE user_string SET value=? WHERE session_id=?",
                       [another_string, cherrypy.session.id])
        """

    def DELETE(self):
        """
        cherrypy.session.pop('ts', None)
        with sqlite3.connect(DB_STRING) as c:
            c.execute("DELETE FROM user_string WHERE session_id=?",
                       [cherrypy.session.id])
        """

def setup_database():
    """
    Create the `user_string` table in the database
    on server startup

    with sqlite3.connect(DB_STRING) as con:
        con.execute("CREATE TABLE user_string (session_id, value)")
    """

def cleanup_database():
    """
    Destroy the `user_string` table from the database
    on server shutdown.

    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE user_string")
    """

if __name__ == '__main__':
    #print os.path.abspath(os.path.dirname(__file__))
    #print os.path.abspath(os.path.dirname(__file__))+'/server'
    conf = {
     '/': {
         'tools.sessions.on': True,
         #'tools.staticdir.root': os.path.abspath(os.getcwd())
         'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__))
        },
     '/expenditures': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
    '/cash': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
       },

     '/static': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': './'+SUB_FOLDER+'/public'
        }
     }

    #cherrypy.engine.subscribe('start', setup_database)
    #cherrypy.engine.subscribe('stop', cleanup_database)

    webapp = Money()
    webapp.expenditures = MoneyWebService()
    webapp.cash = CashWebService(db)
    cherrypy.quickstart(webapp, '/', conf)
