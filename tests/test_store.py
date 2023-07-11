import unittest

from annotass.store import Store

class Context:
    pass

ctx = Context()
ctx.store_fname = "test_store.sqlite"

class TestTrue(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.store = Store(ctx)
        self.store.open()
        self.store.create_table()

    def test_true(self):
        self.assertEqual(True, True, "true")

    @classmethod
    def tearDownClass(self):
        self.store.close()


if __name__ == '__main__':
    unittest.main()