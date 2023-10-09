from flask import Flask, request, make_response, abort
from parse import Parse
from context import Context

import sys

ctx = Context()

try:
    arg = sys.argv[1]
except IndexError:
    arg = ctx.manifest_url

parse = Parse(ctx)
parse.run(url=arg)

app = Flask(__name__)

@app.route('/version')
def version(): return {"version": ctx.version}

@app.route('/search')
def search():
    q = request.args.get('q')
    if q == None: abort(404)
    motivation = request.args.getlist(key='motivation')
    date = request.args.get('date')
    user = request.args.get('user')
    distance = request.args.get('distance', 1.0, type=float)
    response = parse.search(q, motivation, date, user, distance)
    custom_response = make_response(response)
    if ctx.cors: custom_response.headers['Access-Control-Allow-Origin'] = '*'
    return custom_response

if __name__ == '__main__':
    app.run(host=ctx.server_ip, debug=ctx.debug, port=ctx.server_port)