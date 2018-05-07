#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

#Program constants
RANDOMIZATION_PREFIX = "analyzer__675j52sa8b4z84"


def get_current_html_state(chrome_handler):
	while True:
		try:
			page_state = chrome_handler.run_cmd("encodeURI(document.body.innerHTML)")
			break
		except ValueError:
			print "Trying get_current_html_state again"
			time.sleep(5)
	
	return page_state
	

def set_current_html_state(chrome_handler, new_state):
	my_cmd = "document.body.innerHTML = decodeURI('{}')".format(new_state)
	res = chrome_handler.run_cmd(my_cmd)
	return res
	
def setb64_current_html_state(chrome_handler, new_state):
	total_chars = len(new_state)
	variable_name = RANDOMIZATION_PREFIX + "_js_newpagestate"
	chrome_handler.run_cmd("{} = '';".format(variable_name))
	chars_done = 0
	for c_i in range(0, len(new_state), 500):
		c = new_state[c_i:c_i+500]
		chrome_handler.run_cmd("{} += {};".format(variable_name, c))
		chars_done = chars_done + 500
		print "Written: {}/{}".format(chars_done, total_chars)
	
	my_cmd = "document.body.innerHTML = atob({})".format(variable_name)
	print "Running command:..."
	print my_cmd
	res = chrome_handler.run_cmd(my_cmd)
	return res
	
def get_current_location(chrome_handler):
	url_location = chrome_handler.run_cmd("location.href")
	return url_location


def get_all_links(chrome_handler):
	total_link_count = chrome_handler.run_cmd("document.getElementsByTagName('a').length")
	for i in range(0, int(total_link_count)):
		getcmd = "document.getElementsByTagName('a')[{}]".format(i)
		link_dst = chrome_handler.run_cmd("document.getElementsByTagName('a')[{}].href".format(i))
		link_info = {"href": link_dst}
		yield link_info

