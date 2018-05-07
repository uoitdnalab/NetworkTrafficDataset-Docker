#!/bin/bash

tcpdump -i eth0 dst port not 5900 and src port not 5900 -w captured_packets.pcap
