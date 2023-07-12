import unittest
import os
import json
from annotass.annotation_store import Store

class Context:
    pass

ctx = Context()
ctx.store_fname = "test_store.sqlite"

uri = "https://foobar"
annotation = '{"foo": "bar"}'

class TestStore(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.store = Store(ctx)
        self.store.open()
        self.store.create_table()

    def test_write_read(self):
        self.store.write(uri, annotation)
        self.store.commit()
        d = self.store.read(uri)
        self.assertEqual(json.dumps(d), annotation, "write/read test")

    def test_write_read_not_found(self):
        self.store.write(uri="foo", annotation=annotation)
        self.store.commit()
        try:
            _ = self.store.read(uri="bar")
        except Exception as e:
            self.assertEqual(str(e), "no record found", "write/read test")


    @classmethod
    def tearDownClass(self):
        self.store.close()
        os.remove(ctx.store_fname)


if __name__ == '__main__':
    unittest.main()