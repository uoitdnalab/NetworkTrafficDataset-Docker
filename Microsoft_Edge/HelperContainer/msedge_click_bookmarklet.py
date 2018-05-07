#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from QEMU_MouseKey import QEMU_MouseKey

PTY_FILE = sys.argv[1]

qm = QEMU_MouseKey(PTY_FILE)
time.sleep(1)
qm.mouse_set_index(3)
time.sleep(1)
qm.mouse_move_abs(20, 40)
time.sleep(1)
qm.left_single_click()
qm.close_pty()
