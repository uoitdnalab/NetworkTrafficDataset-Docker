#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

PIPE_FILE = sys.argv[1]

f_pipe = open(PIPE_FILE, 'r')
f_pipe.readline() #Wait for an acknowledgement to go forward
f_pipe.flush()
f_pipe.close()
