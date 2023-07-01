import requests_cache
from parse import Parse

class Context:
    pass

ctx = Context()
ctx.session = requests_cache.CachedSession("annotass_cache")


p = Parse(ctx)
collection = p.get_collection(url='https://miiifystore.s3.eu-west-2.amazonaws.com/iiif/collection.json')
p.collection(collection)
