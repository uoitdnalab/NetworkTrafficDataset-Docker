#!/bin/bash

cd /
echo -ne '\n\n\n\n\nremote.localcontrol\n\n\n' | openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
