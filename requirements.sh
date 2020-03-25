#!/bin/bash

if [[ "$(python3 -V)" =~ "Python 3" ]]; then
   	
	sudo pip3 install numpy
    sudo pip3 install opencv-python
    sudo pip3 install opencv-contrib-python
else 
    echo "Python3 or above not installed"
fi
