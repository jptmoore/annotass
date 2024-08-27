import os

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

@app.route('/ok')
def ok():
    return 'OK'

@app.route('/search')
def search():
    q = request.args.get('q')
    if q == None: abort(404)
    motivation = request.args.getlist(key='motivation')
    date = request.args.get('date')
    user = request.args.get('user')
    n = request.args.get('n', ctx.annotation_limit, type=int)
    if n < 1 or n > ctx.annotation_limit: abort(404)
    distance = request.args.get('distance', ctx.cosine_distance, type=float)
    if distance < 0.0 or distance > 2.0: abort(404) 
    response = parse.search(q, motivation, date, user, n, distance)
    custom_response = make_response(response)
    if ctx.cors: custom_response.headers['Access-Control-Allow-Origin'] = '*'
    return custom_response

if __name__ == '__main__':
    app.run(host=ctx.server_ip, debug=ctx.debug, port=int(os.getenv('PORT', ctx.server_port)))