#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import hashlib
import time
import base64

import networkx as nx
from bs4 import BeautifulSoup

import PageStateUtils
import DOMUtilities
from ChromeHandler import ChromeHandler

DOM_DIR = "__doms"
RANDOMIZATION_PREFIX = "analyzer__675j52sa8b4z84"

NETGRAPH_FILE = sys.argv[1]
NODE_URL = sys.argv[2]
IN_DOCKER = bool("in_docker" == sys.argv[3])

#Load the NetworkX graph
G = nx.read_yaml(NETGRAPH_FILE)

#Load Chrome... and the website
chrome_driver = ChromeHandler(NODE_URL, IN_DOCKER)

time.sleep(20)

#Get the page state
page_state = PageStateUtils.get_page_html(chrome_driver)

#unique_tagged = PageStateUtils.assign_uuids(page_state)
unique_tagged = PageStateUtils.get_unique_tagged_page(chrome_driver, 5)

modified_dom = BeautifulSoup(unique_tagged)

#Get the sha256 hash for the DOM
hasher = hashlib.sha256()
hasher.update(modified_dom.encode())
dom_hash = hasher.hexdigest()

#Get all page links
for lnk in modified_dom.findAll('a'):
	if 'class' not in lnk.attrs:
		continue
	
	classes = lnk['class']
	unique_class = None
	for cls in classes:
		if RANDOMIZATION_PREFIX in cls:
			unique_class = cls
	
	if unique_class is None:
		continue
	
	if 'href' in lnk.attrs:
		link_href = lnk['href']
		#G.add_edge(NODE_URL, link_href, current_page_domhash=dom_hash, uuid=unique_class)
		unresolved_id = "({})-->({})".format(dom_hash, unique_class)
		G.add_edge(dom_hash, unresolved_id, current_page_domhash=dom_hash, uuid=unique_class)



#Save the Document Object Model for this page
f_dom = open("{}/{}.pagedom".format(DOM_DIR, dom_hash), 'w')
f_dom.write(base64.b64encode(modified_dom.encode()))
f_dom.close()

#Save the graph
nx.write_yaml(G, NETGRAPH_FILE)
