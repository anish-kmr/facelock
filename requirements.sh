#!/bin/bash

if [[ "$(python3 -V)" =~ "Python 3" ]]; then
   	
    sudo python3 -m  pip install numpy
    sudo python3 -m pip install opencv-python
    sudo python3 -m pip install opencv-contrib-python
else 
    echo "Python3 or above not installed"
fi
