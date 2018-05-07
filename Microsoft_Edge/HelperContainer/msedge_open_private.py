#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from QEMU_MouseKey import QEMU_MouseKey

PTY_FILE = sys.argv[1]

qm = QEMU_MouseKey(PTY_FILE)
time.sleep(1)
qm.control_shift_key('p')
time.sleep(10)
qm.alt_space()
print "Send ALT-SPACE"
time.sleep(2)
qm.type_string('x')
qm.close_pty()
