#!/bin/bash

export DISPLAY=:0
xset s off
xset -dpms
xset s noblank
cd src/
python transittracker.py -d -s 53656 &
