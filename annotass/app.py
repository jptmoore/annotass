import requests_cache
from parse import Parse

class Context:
    pass

ctx = Context()
ctx.session = requests_cache.CachedSession("cache_annotass.sqlite")
ctx.index_fname = "index_annotass"
ctx.store_fname = "store_annotass.sqlite"

parse = Parse(ctx)
parse.run(url='https://miiifystore.s3.eu-west-2.amazonaws.com/iiif/collection.json')