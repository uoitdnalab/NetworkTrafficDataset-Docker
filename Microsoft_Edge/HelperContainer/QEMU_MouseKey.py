#!/usr/bin/env python
# -*- coding: utf-8 -*-

LEFTMOST = -10000
TOPMOST = - 10000
INTER_CLICK_TIME = 0.250
INTER_KEYSTROKE_TIME = 0.250

import time

REMAP_TABLE = {}
REMAP_TABLE[';'] = 'semicolon'
REMAP_TABLE[':'] = 'shift-semicolon'
REMAP_TABLE['/'] = 'slash'
REMAP_TABLE['.'] = 'dot'

def remap_to_sendkey_char(c):
	if c not in REMAP_TABLE:
		return c
	else:
		return REMAP_TABLE[c]

class QEMU_MouseKey:
	def __init__(self, pts_filename):
		self.f_pts = open(pts_filename, "wb+", buffering=0)
		welcome_msg = self.f_pts.readline()
		print welcome_msg
	
	#def mice_info(self):
	#	self.f_pts.write("info mice\r\n")
	#	while True:
	#		print self.f_pts.readline()
	
	def mouse_to_top_left(self):
		self.f_pts.write("mouse_move {} {}\r\n".format(LEFTMOST, TOPMOST))
		self.f_pts.flush()
	
	def mouse_move_rel(self, dx, dy):
		self.f_pts.write("mouse_move {} {}\r\n".format(dx, dy))
		self.f_pts.flush()
	
	def mouse_move_abs(self, x, y):
		time.sleep(1)
		self.mouse_to_top_left()
		time.sleep(1)
		self.mouse_move_rel(x, y)
		time.sleep(1)
	
	def left_single_click(self):
		time.sleep(INTER_CLICK_TIME)
		self.f_pts.write("mouse_button 1\r\n")
		self.f_pts.flush()
		time.sleep(INTER_CLICK_TIME)
		self.f_pts.write("mouse_button 0\r\n")
		time.sleep(INTER_CLICK_TIME)
		self.f_pts.flush()
	
	def mouse_set_index(self, idx):
		time.sleep(1)
		self.f_pts.write("mouse_set {}\r\n".format(idx))
		time.sleep(1)
	
	def press_enter(self):
		time.sleep(INTER_KEYSTROKE_TIME)
		self.f_pts.write("sendkey kp_enter\r\n")
		self.f_pts.flush()
		time.sleep(INTER_KEYSTROKE_TIME)
	
	def type_string(self, mystr):
		for c in mystr:
			time.sleep(INTER_KEYSTROKE_TIME)
			qemu_char = remap_to_sendkey_char(c)
			self.f_pts.write("sendkey {}\r\n".format(qemu_char))
			self.f_pts.flush()
	
	def control_key(self, key):
		time.sleep(1)
		self.f_pts.write("sendkey ctrl-{}\r\n".format(key))
		self.f_pts.flush()
		time.sleep(1)

	def control_shift_key(self, key):
		time.sleep(1)
		self.f_pts.write("sendkey ctrl-shift-{}\r\n".format(key))
		self.f_pts.flush()
		time.sleep(1)
	
	def alt_space(self):
		time.sleep(1)
		self.f_pts.write("sendkey alt-spc\r\n")
		self.f_pts.flush()
		time.sleep(1)
		
	def alt_f4(self):
		time.sleep(1)
		self.f_pts.write("sendkey alt-f4\r\n")
		self.f_pts.flush()
		time.sleep(1)
		
	def take_screenshot(self, absfilepath):
		time.sleep(1)
		self.f_pts.write("screendump {}\r\n".format(absfilepath))
		self.f_pts.flush()
		time.sleep(1)
	
	def close_pty(self):
		self.f_pts.close()
	
