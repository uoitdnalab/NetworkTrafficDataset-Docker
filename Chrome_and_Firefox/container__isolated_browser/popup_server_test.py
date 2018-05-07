#!/usr/bin/env python
# -*- coding: utf-8 -*-

from popup_server import PopupServerThread


my_server_thread = PopupServerThread("document.body.innerHTML = 'hello world'")
my_server_thread.start()

print "My server thread is running"

my_server_thread.join()

print "My server thread has stopped"
