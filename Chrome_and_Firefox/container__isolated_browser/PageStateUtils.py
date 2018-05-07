#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import base64

from bs4 import BeautifulSoup

import DOMUtilities


#Program constants
RANDOMIZATION_PREFIX = "analyzer__675j52sa8b4z84"
LABEL_TOP_N_JS_FILENAME = "oneline_label_top_n.min.js"

LABEL_TOP_N_JS = ""
f_js = open(LABEL_TOP_N_JS_FILENAME, 'r')
LABEL_TOP_N_JS = f_js.read().rstrip('\n')
f_js.close()

def get_page_html(chrome_handler):
	page_encoded = DOMUtilities.get_current_html_state(chrome_handler)
	page = urllib2.unquote(str(page_encoded))
	
	return page


def assign_uuids(html_page):
	page_soup = BeautifulSoup(html_page)
	page_anchors = page_soup.findAll('a')
	for anchor_index in range(0,len(page_anchors)):
		anchor_name = RANDOMIZATION_PREFIX + "_HTMLa_" + str(anchor_index)
		if 'class' not in page_anchors[anchor_index].attrs:
			page_anchors[anchor_index]['class'] = anchor_name
		else:
			page_anchors[anchor_index]['class'].append(anchor_name)
	
	return page_soup.prettify()


def set_page_html(chrome_handler, html_page):
	page_encoded = base64.b64encode(html_page)
	DOMUtilities.setb64_current_html_state(chrome_handler, page_encoded)


def get_unique_tagged_page(chrome_handler, n_links):
	#Run the JS command
	chrome_handler.run_cmd("eval({})({})".format(LABEL_TOP_N_JS, n_links))
	page_encoded = DOMUtilities.get_current_html_state(chrome_handler)
	page = urllib2.unquote(str(page_encoded))
	return page
	
