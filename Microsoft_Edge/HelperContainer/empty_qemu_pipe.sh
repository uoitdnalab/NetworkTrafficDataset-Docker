#!/bin/bash

cat /qemu_host_pty &
CATPID=$!
sleep 15
kill $CATPID
