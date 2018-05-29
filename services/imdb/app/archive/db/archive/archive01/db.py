from os import path
import sqlite3


class dB:

    def __init__(self, database=":memory:"):
        self.db = database

    def connect(self):
        """
        Parameters:

        Returns:
        :db connection:
        """
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row 
        return conn

    def query(self, query, args=()):
        """
        Parameters:
        :query:             sql statement

        Returns:
        :tuples:            db query output

        query = "select * from "
        """
        conn = self.connect()
        c = conn.cursor()
        c.execute(query, args).fetchall()
        c.close()

        return pd.read_sql_query(query, self.connect())

    def insert(self, table, df):
        """
        Parameters:
        :table:
        :df:

        Returns:
        """
        conn = self.connect()
        cursor = conn.cursor()
        df.to_sql(table, cursor)


if __name__ == '__main__':

    db = dB()
    


