#!/bin/bash

Xvnc :0 -rfbauth /mypass -geometry 1280x720 -depth 16 &
export DISPLAY=:0
sleep 5
jwm &
sleep 5
export SSLKEYLOGFILE=/ssl.log
export MOZ_LOG=timestamp,rotate:200,nsHttp:3,nsSocketTransport:3,nsHostResolver:5
export MOZ_LOG_FILE=/http_log.log
firefox
bash
