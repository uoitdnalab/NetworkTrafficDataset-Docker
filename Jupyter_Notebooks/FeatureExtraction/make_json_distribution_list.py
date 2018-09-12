#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
from scapy.all import *

PCAP_DIRNAME = sys.argv[1]
JSON_NAME = sys.argv[2]

session_sizes_table = {}
maxsize = 0
for root, directories, filenames in os.walk(PCAP_DIRNAME):
	for filename in filenames:
		print os.path.join(root, filename)
		if filename not in session_sizes_table:
			#Get the size of filename
			try:
				pkt_cap = rdpcap(os.path.join(root, filename))
			except scapy.error.Scapy_Exception:
				continue
			
			for pkt in pkt_cap:
				if len(pkt) > maxsize:
					maxsize = len(pkt)

print "Maxsize = {}".format(maxsize)

for root, directories, filenames in os.walk(PCAP_DIRNAME):
	for filename in filenames:
		print os.path.join(root, filename)
		if filename not in session_sizes_table:
			#Get the size of filename
			try:
				pkt_cap = rdpcap(os.path.join(root, filename))
			except scapy.error.Scapy_Exception:
				continue
			
			packet_type_counts = [0]*maxsize
			for pkt in pkt_cap:
				print len(pkt)
				packet_type_counts[len(pkt)] += 1
		
		session_sizes_table[filename] = packet_type_counts[:]

#Save the object
f_json = open(JSON_NAME, 'w')
f_json.write(json.dumps(session_sizes_table))
f_json.close()
