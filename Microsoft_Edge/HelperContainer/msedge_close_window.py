#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from QEMU_MouseKey import QEMU_MouseKey

PTY_FILE = sys.argv[1]

qm = QEMU_MouseKey(PTY_FILE)
time.sleep(1)
#qm.alt_space()
qm.alt_f4()
time.sleep(2)
#qm.type_string('c')
qm.close_pty()
