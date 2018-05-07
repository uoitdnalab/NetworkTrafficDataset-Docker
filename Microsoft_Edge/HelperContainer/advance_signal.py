#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

PIPE_FILE = sys.argv[1]

f_pipe = open(PIPE_FILE, 'w')
f_pipe.write('\n')
f_pipe.flush()
f_pipe.close()
