#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from flask import Flask, Response, request


class PopupServerThread(threading.Thread):
	def __init__(self, cmd_str):
		threading.Thread.__init__(self)
		self.cmd_str = cmd_str
		self.i_am_running = True
	
	def run(self):
		app = Flask(__name__)
		
		@app.route("/")
		def root_page():
			return "This is the root page"
		
		@app.route("/example")
		def example_page():
			return "javascript:alert('Hello world')"
		
		@app.route("/cmd")
		def cmd_page():
			self.i_am_running = False
			resp = Response(self.cmd_str)
			resp.headers['Access-Control-Allow-Origin'] = '*'
			#Shutdown server when we are done
			shutdown_func = request.environ.get('werkzeug.server.shutdown')
			shutdown_func()
			return resp
		
		app.run()
		print "Server has closed"
	
	def isRunning(self):
		return self.i_am_running
		

		
		
