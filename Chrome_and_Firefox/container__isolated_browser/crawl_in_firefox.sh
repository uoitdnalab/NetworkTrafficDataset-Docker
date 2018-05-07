#!/bin/bash

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

#Generate all possible user interaction sequences
#TODO

#Iterate through each user interaction sequence...TODO
	
	#Open a new Private Window
	open_private
	
	#Load the about:blank page
	load_about_blank
	
	#Start to capture network traffic
	./capture_command.sh &
	capture_pid=$!
	sleep 10
	
	#Click the Run Command button
	click_run_command
	
	#Wait
	sleep 45
	
	#Stop the capture of network traffic
	pkill -P $capture_pid
	sleep 5
	
	#Save the captured_packets
	#TODO: Derive the filename
	
	#Close this window
	close_private
	
