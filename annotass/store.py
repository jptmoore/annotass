import sqlite3
import os, os.path

class Store:
    def __init__(self, ctx):
        self.conn = None
        self.store_fname = ctx.store_fname
        if os.path.exists(ctx.store_fname):
            os.remove(ctx.store_fname)

    def open(self):
        self.conn = sqlite3.connect(self.store_fname)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('create table annotations (uri TEXT PRIMARY KEY, data JSON);')

    def write(self, uri, annotation):
        cursor = self.conn.cursor()
        sql = f"insert into annotations (uri, data) values (?, ?);"
        cursor.execute(sql, (uri, annotation))

    def read(self, uri):
        cursor = self.conn.cursor()
        sql = f"select data from annotations where uri = :uri;"
        cursor.execute(sql, {"uri": uri})
        row = cursor.fetchone()
        match row:
            case (x,):
                return x
            case _:
                raise('ouch')

    def commit(self):
        self.conn.commit()   

    def close(self):
        self.conn.close()
