#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

INPUT_JSON_NAME = sys.argv[1]
OUTPUT_JSON_NAME = sys.argv[2]

f_json = open(INPUT_JSON_NAME, 'r')
session_sizes_table = json.loads(f_json.read())
f_json.close()

smallest_size = None
largest_size = None

#Find the smallest and largest sizes
for key in session_sizes_table:
	if smallest_size == None:
		smallest_size = session_sizes_table[key]
	if largest_size == None:
		largest_size = session_sizes_table[key]
	
	if session_sizes_table[key] < smallest_size:
		smallest_size = session_sizes_table[key]
	
	if session_sizes_table[key] > largest_size:
		largest_size = session_sizes_table[key]
	

#Normalize
new_table = {}
for key in session_sizes_table:
	new_table[key] = float(session_sizes_table[key] - smallest_size) / float(largest_size - smallest_size)

#Save
f_json = open(OUTPUT_JSON_NAME, 'w')
f_json.write(json.dumps(new_table))
f_json.close()
