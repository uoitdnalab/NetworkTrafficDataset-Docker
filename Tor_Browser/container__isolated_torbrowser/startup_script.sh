#!/bin/bash

Xvnc :0 -rfbauth /home/anon/mypass -geometry 1280x720 -depth 16 &
export DISPLAY=:0
sleep 5
jwm &
sleep 5
su anon -c torbrowser-launcher &
bash
