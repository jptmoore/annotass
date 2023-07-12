import sqlite3
import os, os.path
import ast

from context import Context

class Store:
    def __init__(self, ctx: Context) -> None:
        self.conn = None
        self.store_fname = ctx.store_fname
        if os.path.exists(ctx.store_fname):
            os.remove(ctx.store_fname)

    def open(self) -> None:
        self.conn = sqlite3.connect(self.store_fname, check_same_thread=False)

    def create_table(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute('create table annotations (uri TEXT PRIMARY KEY, data JSON);')

    def write(self, uri: str, annotation: str) -> None:
        cursor = self.conn.cursor()
        sql = f"insert into annotations (uri, data) values (?, ?);"
        cursor.execute(sql, (uri, annotation))

    def read(self, uri: str) -> dict[str, object]: 
        cursor = self.conn.cursor()
        sql = f"select data from annotations where uri = :uri;"
        cursor.execute(sql, {"uri": uri})
        row = cursor.fetchone()
        match row:
            case None:
                raise Exception('no record found')
            case (x,):
                return ast.literal_eval(x)
            case _:
                raise Exception('error retrieving row')

    def commit(self) -> None:
        self.conn.commit()   

    def close(self) -> None:
        self.conn.close()
