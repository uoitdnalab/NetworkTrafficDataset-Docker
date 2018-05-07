#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from QEMU_MouseKey import QEMU_MouseKey

PTY_FILE = sys.argv[1]

qm = QEMU_MouseKey(PTY_FILE)
qm.control_key('l')
#qm.type_string('about:blank')
qm.type_string('file:///c:/users/ieuser/documents/blank.html')
qm.press_enter()
qm.close_pty()
