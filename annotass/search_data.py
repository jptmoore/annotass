import os, os.path
from whoosh.index import create_in
from whoosh.fields import Schema, ID, TEXT
from whoosh.qparser import QueryParser

from context import Context


class Data:
    def __init__(self, ctx: Context) -> None:
        self.index_fname = ctx.index_fname
        self.annotation_limit = ctx.annotation_limit
        self.schema = Schema(id=ID(stored=True), content=TEXT)
        self.idx = None

    def write_data(self, id: str, content: str) -> None:
        writer = self.idx.writer()
        writer.add_document(id=id, content=content)
        writer.commit()       

    def create_index(self):
        if not os.path.exists(self.index_fname):
            os.mkdir(self.index_fname)
        idx = create_in(self.index_fname, self.schema)
        self.idx = idx
        return idx 


    def search_data(self, term: str, page: int) -> None:
        try:
            if page < 0: return (0, [])
            qp = QueryParser("content", schema=self.idx.schema)
            query = qp.parse(term)
            with self.idx.searcher() as s:
                page_length = self.annotation_limit
                results = s.search_page(query, page+1, pagelen=page_length)
                results_length = len(results)
                if page > (results_length / page_length): return (0, [])
                uris = []
                for r in results:
                    uri = r.get('id')
                    uris.append(uri)
                result = (results_length, uris)
        except Exception as e:
            print("ouch")
        else:
            return result
        


