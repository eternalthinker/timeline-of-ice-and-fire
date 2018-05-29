from os import path
from sqlite3 import dbapi2 as sqlite3 
from flask import g

DATABASE = 'got.db'


# http://flask.pocoo.org/docs/0.11/patterns/sqlite3/#sqlite3
def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row 
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return(rv[0] if rv else None) if one else rv


# https://stackoverflow.com/questions/2092757/python-and-sqlite-insert-into-table
def insert(cursor, table, row):
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    cursor.execute(sql, row)


def update(cursor, table, row):
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'UPDATE "{0}" SET ({1}) VALUES ({2}) WHERE {4}'.format(table, cols, vals)
    cursor.execute(sql, row)