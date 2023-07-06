from flask import Flask, request, make_response, abort
from parse import Parse
from configparser import ConfigParser

config_ini = ConfigParser()
config_ini.read("config.ini")

class Context:
    pass

ctx = Context()
ctx.version = config_ini.get("main", "VERSION")
ctx.annotation_limit = config_ini.getint("annotass", "ANNOTATION_LIMIT")
ctx.cache_fname = config_ini.get("annotass", "CACHE_FNAME")
ctx.index_fname = config_ini.get("annotass", "INDEX_FNAME")
ctx.store_fname = config_ini.get("annotass", "STORE_FNAME") 
ctx.server_port = config_ini.getint("annotass", "SERVER_PORT")
ctx.debug = config_ini.getboolean("annotass", "DEBUG")
ctx.cors = config_ini.getboolean("annotass", "CORS")
ctx.search_url = "https://miiify.rocks/iiif/content/search"

parse = Parse(ctx)
#parse.run(url='https://miiifystore.s3.eu-west-2.amazonaws.com/iiif/collection.json')
parse.run(url='https://miiify.rocks/manifest/cats')


app = Flask(__name__)

@app.route('/search')
def search():
    q = request.args.get('q')
    if q == None: abort(404)
    page = request.args.get('page', 0, type=int)
    response = parse.search(q, page)
    custom_response = make_response(response)
    if ctx.cors: custom_response.headers['Access-Control-Allow-Origin'] = '*'
    return custom_response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=ctx.debug, port=ctx.server_port)