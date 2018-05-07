#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx

NETGRAPH_FILE = sys.argv[1]
MAIN_URL = sys.argv[2]
COMMANDS_DIR = sys.argv[3]


def get_center_node(graph):
	for nd in graph.nodes():
		if graph.in_degree(nd) == 0 and graph.out_degree(nd) > 0:
			return nd



def emit_code__set_dir(node):
	cmd_str = """
mkdir ROUTE_TO__{}
cd ROUTE_TO__{}
	""".format(node, node)
	return cmd_str

def emit_code__main():
	cmd_str = """
open_private
load_about_blank
echo 'window.location = "{}"' > next_jscmd
while nc -z 127.0.0.1 5000; do sleep 1; echo 'waiting for port 5000 to be open'; done; echo 'port 5000 is open'
python /command_server.py next_jscmd &
sleep 10
click_run_command
sleep 45
	""".format(MAIN_URL)
	return cmd_str


def emit_code__closeprivate():
	cmd_str = """
sleep 10
close_private
sleep 10
	"""
	return cmd_str

def emit_code__load(parent_node):
	cmd_str = """
while nc -z 127.0.0.1 5000; do sleep 1; echo 'waiting for port 5000 to be open'; done; echo 'port 5000 is open'
python /dom_set_server.py /__doms/{}.pagedom &
sleep 10
click_run_command
sleep 45
take_screenshot /__screenshots/{}.png
	""".format(parent_node, parent_node)
	return cmd_str

def emit_code__begin_cap(child_node):
	cmd_str = """
/capture_command.sh &
capture_pid=$!
sleep 10
	"""
	return cmd_str

def emit_code__end_cap(child_node):
	cmd_str = """
pkill -P $capture_pid
sleep 5
mv captured_packets.pcap {}.pcap
	""".format(child_node)
	return cmd_str
	
def emit_code__exec(uuid):
	cmd_str = """
echo 'document.getElementsByClassName("{}")[0].click()' > next_jscmd
while nc -z 127.0.0.1 5000; do sleep 1; echo 'waiting for port 5000 to be open'; done; echo 'port 5000 is open'
python /command_server.py next_jscmd &
sleep 10
click_run_command
sleep 45
	""".format(uuid)
	return cmd_str


def emit_firefox_script_header():
	cmd_str = """#!/bin/bash

export DISPLAY=:0

#Open a new private window in Firefox
open_private(){
	xte 'key Alt_L'
	sleep 1
	xte 'key f'
	sleep 1
	xte 'key w'
	sleep 1
}

#Close the private window
close_private(){
	xte 'key Alt_L'
	sleep 1
	xte 'key f'
	sleep 1
	xte 'key d'
	sleep 15
}

load_about_blank(){
	xte 'keydown Control_L'
	sleep 1
	xte 'key l'
	sleep 1
	xte 'keyup Control_L'
	sleep 1
	xte 'str about:blank'
	sleep 1
	xte 'key Return'
	sleep 5
}

click_run_command(){
	sleep 1
	xte 'mousemove 50 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

take_screenshot(){
	scrot $1
}

	"""
	return cmd_str


def emit_chrome_script_header():
	cmd_str = """#!/bin/bash

export DISPLAY=:0

#Open a new private window in Chrome
open_private(){
	xte 'keydown Control_L'
	sleep 1
	xte 'keydown Shift_L'
	sleep 1
	xte 'key n'
	sleep 1
	xte 'keyup Shift_L'
	sleep 1
	xte 'keyup Control_L'
	sleep 1
}

#Close the private window
close_private(){
	xte 'keydown Control_L'
	sleep 1
	xte 'key w'
	sleep 1
	xte 'keyup Control_L'
	sleep 15
}

load_about_blank(){
	xte 'keydown Control_L'
	sleep 1
	xte 'key l'
	sleep 1
	xte 'keyup Control_L'
	sleep 1
	xte 'str about:blank'
	sleep 1
	xte 'key Return'
	sleep 5
}

click_run_command(){
	sleep 1
	xte 'mousemove 50 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

take_screenshot(){
	scrot $1
}

	"""
	return cmd_str


def emit_brave_script_header():
	cmd_str = """#!/bin/bash

export DISPLAY=:0

#Open a new private window in Brave
open_private(){
	brave &
	sleep 60
	xte 'keydown Control_L'
	sleep 1
	xte 'key n'
	sleep 1
	xte 'keyup Control_L'
	
	sleep 5
	
	xte 'keydown Control_L'
	sleep 1
	xte 'keydown Shift_L'
	sleep 1
	xte 'key p'
	sleep 1
	xte 'keyup Shift_L'
	sleep 1
	xte 'keyup Control_L'
	sleep 1
}

#Close the private window
close_private(){
	xte 'keydown Control_L'
	sleep 1
	xte 'key w'
	sleep 1
	xte 'keyup Control_L'
	sleep 15
	killall brave
	sleep 60
}

load_about_blank(){
	xte 'keydown Control_L'
	sleep 1
	xte 'key l'
	sleep 1
	xte 'keyup Control_L'
	sleep 1
	xte 'str file:///home/ubuntu/blank.html'
	sleep 1
	xte 'key Return'
	sleep 5
}

click_run_command(){
	sleep 1
	xte 'mousemove 50 70'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

take_screenshot(){
	scrot $1
}

	"""
	return cmd_str



def emit_edge_script_header():
	cmd_str = """#!/bin/bash

export DISPLAY=:0

PTY_FILE=/qemu_host_pty

#Open a new private window in Chrome
open_private(){
	sleep 1
	/empty_qemu_pipe.sh
	sleep 1
	python /msedge_open_private.py $PTY_FILE
	sleep 5
}

#Close the private window
close_private(){
	sleep 1
	/empty_qemu_pipe.sh
	sleep 1
	python /msedge_close_window.py $PTY_FILE
	sleep 5
}

load_about_blank(){
	sleep 1
	/empty_qemu_pipe.sh
	sleep 1
	python /msedge_navigate_aboutblank.py $PTY_FILE
	sleep 5
}

click_run_command(){
	sleep 1
	/empty_qemu_pipe.sh
	sleep 1
	python /msedge_click_bookmarklet.py $PTY_FILE
	sleep 5
}

take_screenshot(){
	sleep 1
	/empty_qemu_pipe.sh
	sleep 1
	python /msedge_take_screenshot.py $PTY_FILE $1
	sleep 1
}

	"""
	return cmd_str


def emit_torbrowser_script_header():
	cmd_str = """#!/bin/bash

export DISPLAY=:0

#Open a new private window in TorBrowser
open_private(){
	xte 'keydown Control_L'
	sleep 1
	xte 'keydown Shift_L'
	sleep 1
	xte 'key p'
	sleep 1
	xte 'keyup Shift_L'
	sleep 1
	xte 'keyup Control_L'
	sleep 5
	wmctrl -r :ACTIVE: -b add,maximized_vert
	sleep 1
	wmctrl -r :ACTIVE: -b add,maximized_horz
	sleep 10
}

#Close the private window
close_private(){
	xte 'key Alt_L'
	sleep 1
	xte 'key f'
	sleep 1
	xte 'key d'
	sleep 15
}

load_about_blank(){
	xte 'keydown Control_L'
	sleep 1
	xte 'key l'
	sleep 1
	xte 'keyup Control_L'
	sleep 1
	xte 'str about:blank'
	sleep 1
	xte 'key Return'
	sleep 5
}

click_run_command(){
	sleep 1
	xte 'mousemove 50 100'
	sleep 1
	xte 'mouseclick 1'
	sleep 1
}

take_screenshot(){
	scrot $1
}

	"""
	return cmd_str


#Load the NetworkX graph
G = nx.read_yaml(NETGRAPH_FILE)

CENTER_NODE = get_center_node(G)

for node in G.nodes():
	if node == CENTER_NODE:
		continue
	
	print "--- BEGIN: instructions to navigate to: {} ---".format(node)
	instructions_list = ""
	
	print "\t SET_DIR {}".format(node)
	instructions_list += emit_code__set_dir(node)
	
	print "\t MAIN"
	instructions_list += emit_code__main()
	
	#Get path from the center node to here
	selectors_path = nx.shortest_path(G, CENTER_NODE, node)
	for i in range(0, len(selectors_path)):
		parent_index = i
		child_index = i + 1
		if child_index >= len(selectors_path):
			break
		parent_node = selectors_path[parent_index]
		child_node = selectors_path[child_index]
		edge_attrs = G.get_edge_data(parent_node, child_node)
		uuid = edge_attrs['uuid']
		#print "\t@{} RUN document.getElementsByClassName('{}')[0].click()".format(parent_node, uuid)
		print "\t LOAD {}".format(parent_node)
		instructions_list += emit_code__load(parent_node)
		
		print "\t BEGIN_CAP {}".format(child_node)
		instructions_list += emit_code__begin_cap(child_node)
		
		print "\t EXEC {}".format(uuid)
		instructions_list += emit_code__exec(uuid)
		
		print "\t END_CAP {}".format(child_node)
		instructions_list += emit_code__end_cap(child_node)
		
	print "--- END: instructions to navigate to: {} ---".format(node)
	print ""
	
	instructions_list += emit_code__closeprivate()
	
	#Save to files
	f_instructions = open("{}/firefox_test_for_{}.sh".format(COMMANDS_DIR, node),'w')
	f_instructions.write(emit_firefox_script_header())
	f_instructions.write(instructions_list)
	f_instructions.close()
	
	f_instructions = open("{}/chrome_test_for_{}.sh".format(COMMANDS_DIR, node),'w')
	f_instructions.write(emit_chrome_script_header())
	f_instructions.write(instructions_list)
	f_instructions.close()
	
	f_instructions = open("{}/edge_test_for_{}.sh".format(COMMANDS_DIR, node),'w')
	f_instructions.write(emit_edge_script_header())
	f_instructions.write(instructions_list)
	f_instructions.close()
	
	f_instructions = open("{}/torbrowser_test_for_{}.sh".format(COMMANDS_DIR, node),'w')
	f_instructions.write(emit_torbrowser_script_header())
	f_instructions.write(instructions_list)
	f_instructions.close()
	
	f_instructions = open("{}/bravebrowser_test_for_{}.sh".format(COMMANDS_DIR, node),'w')
	f_instructions.write(emit_brave_script_header())
	f_instructions.write(instructions_list)
	f_instructions.close()
