#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from PIL import Image

from QEMU_MouseKey import QEMU_MouseKey

PTY_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

qm = QEMU_MouseKey(PTY_FILE)
qm.take_screenshot("/tmp/screenshot_from_qemu_msedge")
time.sleep(2)
qm.close_pty()

#Convert the PPM file
im = Image.open("/tmp/screenshot_from_qemu_msedge")
im.save(OUTPUT_FILE, "PNG")
