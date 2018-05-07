#!/bin/bash

pcap_count=0
while true
do
	#Wait for the signal to begin recording traffic
	python block_wait.py capture_ctrl
	
	#Signal has been received, therefore capture traffic
	tcpdump -i tap0 -w captured_packets.pcap &
	capture_pid=$!
	
	#Wait for the signal to stop recording traffic
	python block_wait.py capture_ctrl
	
	#Signal has been received, therefore stop TCPDUMP process
	pkill -P $capture_pid
	
	pcap_count=$((pcap_count + 1))
	
	#Name the pcap file
	#mv captured_packets.pcap "captured_packets_$pcap_count.pcap"
	
done
