import requests_cache
from parse import Parse

from store import Store

class Context:
    pass

ctx = Context()
ctx.session = requests_cache.CachedSession("cache_annotass.sqlite")
ctx.index_fname = "index_annotass"
ctx.db_name = "store_annotass.sqlite"

# parse = Parse(ctx)
# parse.run(url='https://miiifystore.s3.eu-west-2.amazonaws.com/iiif/collection.json')

store = Store(ctx)
store.open()
store.write(uri='foo', annotation='{\"json1\": \"works\"}')
store.close()