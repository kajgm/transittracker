#!/bin/bash
export DISPLAY=:0
xset s off
xset -dpms
xset s noblank

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
python3.10 src/transittracker.py -df &
