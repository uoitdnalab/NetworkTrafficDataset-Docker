#!/bin/bash

cd /
tar -xvf scapy-2.4.0.tar.gz
cd /scapy-2.4.0
./setup.py build
./setup.py install
