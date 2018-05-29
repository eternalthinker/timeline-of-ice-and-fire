from os import path
from sqlite3 import dbapi2 as sqlite3 

DATABASE = 'got.db'


class dB:

    def __init__(self, database=':memory:'):
        self.database = database

    def connect(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, cursor, table, row):
        columns = ', '.join(row.keys())
        placeholders = ' ,'.join('?' * len(row))
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, columns, placeholders)
        cursor.execute(sql, tuple(row.values()))
