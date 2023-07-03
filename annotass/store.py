import sqlite3
import os, os.path
class Store:
    def __init__(self, ctx):
        if os.path.exists(ctx.store_fname):
            os.remove(ctx.store_fname)
        self.conn = sqlite3.connect(ctx.store_fname)

    def open(self):
        cursor = self.conn.cursor()
        cursor.execute('create table annotations (uri TEXT PRIMARY KEY, data JSON);')

    def write(self, uri, annotation):
        cursor = self.conn.cursor()
        sql = f"insert into annotations (uri, data) values ('{uri}', json('{annotation}'));"
        cursor.execute(sql)

    def close(self):
        self.conn.commit()
        self.conn.close()

