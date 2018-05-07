#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Flask, Response, request

dom_filename = sys.argv[1]

f_dom = open(dom_filename, 'r')
dom_contents = f_dom.read().rstrip('\n')
f_dom.close()

js_dom_set = "document.body.innerHTML = atob('{}')".format(dom_contents)

app = Flask(__name__)

@app.route("/")
def root_page():
	return "This is the root page"

@app.route("/example")
def example_page():
	return "javascript:alert('Hello world')"

@app.route("/cmd")
def cmd_page():
	resp = Response(js_dom_set)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	#Shutdown server when we are done
	shutdown_func = request.environ.get('werkzeug.server.shutdown')
	shutdown_func()
	return resp

if __name__ == "__main__":
	app.run()

