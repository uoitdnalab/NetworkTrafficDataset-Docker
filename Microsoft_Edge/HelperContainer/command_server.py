#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Flask, Response, request

js_cmd_filename = sys.argv[1]

app = Flask(__name__)

@app.route("/")
def root_page():
	return "This is the root page"

@app.route("/example")
def example_page():
	return "javascript:alert('Hello world')"

@app.route("/cmd")
def cmd_page():
	f_js = open(js_cmd_filename, 'r')
	js_cmds = f_js.readline().rstrip('\n')
	f_js.close()
	resp = Response(js_cmds)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	#Shutdown server when we are done
	shutdown_func = request.environ.get('werkzeug.server.shutdown')
	shutdown_func()
	return resp

if __name__ == "__main__":
	app.run(host='0.0.0.0', ssl_context=('/cert.pem', '/key.pem'))

