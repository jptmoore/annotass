from flask import Flask, request, make_response, abort
from parse import Parse

class Context:
    pass

ctx = Context()
ctx.cache_fname = "cache_annotass.sqlite"
ctx.index_fname = "index_annotass"
ctx.store_fname = "store_annotass.sqlite"
ctx.annotation_limit = 10
ctx.search_url = "https://miiify.rocks/iiif/content/search"

parse = Parse(ctx)
parse.run(url='https://miiifystore.s3.eu-west-2.amazonaws.com/iiif/collection.json')

app = Flask(__name__)

@app.route('/search')
def search():
    q = request.args.get('q')
    if q == None: abort(404)
    page = request.args.get('page', 0, type=int)
    response = parse.search(q, page)
    custom_response = make_response(response)
    return custom_response

if __name__ == '__main__':
    app.run(host='0.0.0.0')