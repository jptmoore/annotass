import unittest
import os
import json
from annotass.store import Store

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
        dict = self.store.read(uri)
        self.assertEqual(json.dumps(dict), annotation, "write/read test")

    @classmethod
    def tearDownClass(self):
        self.store.close()
        os.remove(ctx.store_fname)


if __name__ == '__main__':
    unittest.main()