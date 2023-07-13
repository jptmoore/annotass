import unittest
import shutil
from annotass.search_data import Data

class Context:
    pass

ctx = Context()
ctx.index_fname = "test_index.sqlite"
ctx.annotation_limit = 10


class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data = Data(ctx)

    def test_write_read(self):
        self.data.create_index()
        self.data.write_data(id="foo", content="hello world")
        x,y = self.data.search_data(term="hello", page=0)
        self.assertEqual(x, 1, 'write/read test')
        self.assertEqual(y, ['foo'], 'write/read test')

    def test_write_read_not_found(self):
        self.data.create_index()
        self.data.write_data(id="foo", content="hello world")
        x,y = self.data.search_data(term="bonjour", page=0)
        self.assertEqual(x, 0, 'write/read test')
        self.assertEqual(y, [], 'write/read not found test')

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(ctx.index_fname)


if __name__ == '__main__':
    unittest.main()