#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal

PIPE_FILE = "/capture_ctrl"

keepRunning = True

def handler(signum, frame):
	print "Stopping packet capture process"
	global keepRunning
	keepRunning = False


#Setup the signal handler
signal.signal(signal.SIGTERM, handler)

#Start the capture
f_pipe = open(PIPE_FILE, 'w')
f_pipe.write('\n')
f_pipe.flush()
f_pipe.close()


#Block - wait for this process to be killed before signaling the end of the capture
while keepRunning:
	pass


#Stop the capture
f_pipe = open(PIPE_FILE, 'w')
f_pipe.write('\n')
f_pipe.flush()
f_pipe.close()
