#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import time
import hashlib
import base64

import networkx as nx
from bs4 import BeautifulSoup

import PageStateUtils

DOM_DIR = "__doms"
BOOKMARKLET_FILE = "bookmarklet.js"
RANDOMIZATION_PREFIX = "analyzer__675j52sa8b4z84"

f_bookmarklet = open(BOOKMARKLET_FILE, 'r')
BOOKMARKLET_DO_CMD = f_bookmarklet.read().rstrip('\n')
f_bookmarklet.close()

NETGRAPH_FILE = sys.argv[1]
NODE_URL = sys.argv[2]
WITH_BROWSER = bool("with_browser" == sys.argv[3])
IN_DOCKER = bool("in_docker" == sys.argv[4])

if WITH_BROWSER:
	import DOMUtilities
	from ChromeHandler import ChromeHandler
	from popup_server import PopupServerThread


def get_leaves(graph):
	for nd in graph.nodes():
		if graph.in_degree(nd) == 1 and graph.out_degree(nd) == 0:
			yield nd

def get_center_node(graph):
	for nd in graph.nodes():
		if graph.in_degree(nd) == 0 and graph.out_degree(nd) > 0:
			return nd

#Load the NetworkX graph
G = nx.read_yaml(NETGRAPH_FILE)

#Get a list of the graph leaves
original_G = G.copy()

#For each leaf get the list of Javascript commands to get there
for leaf in get_leaves(original_G):
	#selectors_path = nx.shortest_path(original_G, NODE_URL, leaf)
	root_node = get_center_node(original_G)
	selectors_path = nx.shortest_path(original_G, root_node, leaf)
	
	js_commands = []
	for node_index in range(0, len(selectors_path)):
		#Get the JS selector associated with this edge
		if node_index + 1 >= len(selectors_path):
			break
		
		parent_node = selectors_path[node_index]
		child_node = selectors_path[node_index + 1]
		this_edge_data = original_G.get_edge_data(parent_node, child_node)
		
		js_cmd = this_edge_data['uuid']
		domhash = this_edge_data['current_page_domhash']
		js_commands.append((domhash, "document.getElementsByClassName('{}')[0].click()".format(js_cmd)))
		
	
	print "To get to {}, run {}".format(leaf, js_commands)
	
	failed_command = False
	
	if WITH_BROWSER:
		print "Please Wait..."
		#This can fail, therefore...try, try, try again
		while True:
			try:
				chrome_driver = ChromeHandler(NODE_URL, IN_DOCKER)
				print "Sucessfully loaded the Chrome Browser"
				break
			except:
				print "Trying again"
				time.sleep(10)
		
		#Exectute the Javascripts commands to get to the leaf...
		for dom_cmd in js_commands:
			dom_hash = dom_cmd[0]
			cmd = dom_cmd[1]
			#Reset the DOM to the state when it was first captured
			dom_set_cmd = 'document.body.innerHTML = atob("'
			
			dom_file = open("{}/{}.pagedom".format(DOM_DIR, dom_hash),'r')
			dom_set_cmd += dom_file.read().rstrip('\n')
			dom_file.close()
			
			dom_set_cmd += '")'
			
			#... serve the appropriate command ...
			my_temp_server = PopupServerThread(dom_set_cmd)
			my_temp_server.start()
			
			#... initiate the XHR request from the browser ...
			while my_temp_server.isRunning():
				chrome_driver.run_cmd(BOOKMARKLET_DO_CMD)
				if my_temp_server.isRunning() == False:
					break
				time.sleep(10)
				print "Bookmarklet command failed!"
				"""
				If we reach here it is because run_cmd did not work,
				therefore prune off this leaf.
				"""
				failed_command = True
				break
			
			#Wait a bit
			time.sleep(10)
			
			#...ensure the popup server has properly closed
			my_temp_server.join()
			print "ServerThread complete"
			
			if failed_command:
				break
			
			#... click the link ...
			chrome_driver.run_cmd(cmd)
			print "Executed: {}".format(cmd)
			
			"""
			f_dom = open("{}/{}.pagedom".format(DOM_DIR, dom_hash),'r')
			this_dom = f_dom.read().rstrip('\n')
			f_dom.close()
			#DOMUtilities.set_current_html_state(chrome_driver, dom)
			DOMUtilities.setb64_current_html_state(chrome_driver, this_dom)
			
			time.sleep(5)
			
			js_res = chrome_driver.run_cmd(cmd)
			print "Result of running the JS command was: {}".format(js_res)
			"""
			
			
			time.sleep(30)
			leaf_url = DOMUtilities.get_current_location(chrome_driver)
			print "Browser URL is: {}".format(leaf_url)
		
		if failed_command:
			print "Something went wrong while navigating to this leaf, therefore removing it."
			G.remove_node(leaf)
			#Close the browser
			chrome_driver.quit_browser()
			print "Closed browser...now waiting..."
			time.sleep(30)
			break
		
		print "Sucessfully navigated to leaf: {}".format(leaf)
		
		#Uniquely tag elements on the page
		page_state = PageStateUtils.get_page_html(chrome_driver)
		
		#unique_tagged = PageStateUtils.assign_uuids(page_state)
		unique_tagged = PageStateUtils.get_unique_tagged_page(chrome_driver, 5)
		
		modified_dom = BeautifulSoup(unique_tagged)
		
		#Get the DOM hash for this uniquely tagged page
		hasher = hashlib.sha256()
		hasher.update(modified_dom.encode())
		dom_hash = hasher.hexdigest()
		
		#Save the uniquely tagged page
		f_dom = open("{}/{}.pagedom".format(DOM_DIR, dom_hash), 'w')
		f_dom.write(base64.b64encode(modified_dom.encode()))
		f_dom.close()
		
		
		#Rename this leaf node to its DOM hash
		nx.relabel_nodes(G, {leaf:dom_hash}, copy=False)
		
		#Save the current state of the graph, G
		nx.write_yaml(G, NETGRAPH_FILE)
		
		#Close the browser
		chrome_driver.quit_browser()
		print "Closed browser...now waiting..."
		time.sleep(30)
