#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib
#import time
import pexpect

CHROME_BASE_CMD = "chromium-browser --headless --disable-gpu --repl {}"
CHROME_DOCKER_BASE_CMD = "chromium-browser --headless --disable-gpu --no-sandbox --repl {}"
PROMPT_CHARS = ">>> "
BLANK_LINE_THRESH = 15

def encode_cmdline_safe_url(_raw_url):
	print "Making a safe URL"
	unquoted_url = ""
	#There shouldn't be any single-quotes in the raw_url
	#but be safe and remove any should there happen to be some
	raw_url = str(_raw_url)
	for c in raw_url:
		if c == "'":
			continue
		else:
			unquoted_url += c
	
	return "'" + unquoted_url + "'"

class ChromeHandler:
	def __init__(self, url, in_docker=False):
		safe_url = encode_cmdline_safe_url(url)
		if in_docker:
			self.chrome_proc = pexpect.spawn(CHROME_DOCKER_BASE_CMD.format(safe_url))
		else:
			self.chrome_proc = pexpect.spawn(CHROME_BASE_CMD.format(safe_url))
		
		#time.sleep(30)
		blank_line_count = 0
		while True:
			myline = self.chrome_proc.readline()
			myline = myline.rstrip('\n')
			myline = myline.rstrip('\r')
			if myline == '':
				print "BLANK LINE"
				blank_line_count += 1
				if blank_line_count > BLANK_LINE_THRESH:
					self.chrome_proc.close(force=True)
					raise Exception("Failed to Start Chrome")
			else:
				print myline
			
			if 'Type a Javascript expression to evaluate or "quit" to exit' in myline:
				break
	
	def run_cmd(self, repl_cmd):
		#Wait for prompt
		#time.sleep(30)
		self.chrome_proc.expect(PROMPT_CHARS)
		
		#time.sleep(0.5)
		
		#Run the command
		self.chrome_proc.sendline(repl_cmd)
		
		#time.sleep(0.5)
		
		#Wait for output
		#print self.chrome_proc.readline()
		self.chrome_proc.readline() #Advance
		
		#time.sleep(0.5)
		#self.chrome_proc.expect(PROMPT_CHARS + repl_cmd + "\r\n")
		
		#Get the output
		while True:
			repl_out = self.chrome_proc.readline()
			if repl_out[0] == '{':
				break
		
		#print repl_out
		
		#Parse output
		repl_out_obj = json.loads(repl_out)
		
		if "result" not in repl_out_obj:
			return -1
		
		if "value" not in repl_out_obj["result"]:
			return -1
		
		return repl_out_obj["result"]["value"]
	
	def quit_browser(self):
		self.chrome_proc.expect(PROMPT_CHARS)
		self.chrome_proc.sendline("quit")
		self.chrome_proc.close(force=True)
		
		
		
