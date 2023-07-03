import sqlite3

class Store:
    def __init__(self, ctx):
        self.conn = sqlite3.connect(ctx.db_name)

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

