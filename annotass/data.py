import os, os.path
from whoosh.index import create_in
from whoosh.fields import *

class Data:
    def __init__(self, ctx):
        self.index_fname = ctx.index_fname
        self.schema = Schema(id=ID(stored=True), content=TEXT)
        self.idx = None

    def write_data(self, id, content):
        writer = self.idx.writer()
        writer.add_document(id=id, content=content)
        writer.commit()       

    def create_index(self):
        if not os.path.exists(self.index_fname):
            os.mkdir(self.index_fname)
        idx = create_in(self.index_fname, self.schema)
        self.idx = idx
        return idx 


        


