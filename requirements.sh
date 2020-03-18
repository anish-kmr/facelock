#!/bin/bash

if [[ "$(python3 -V)" =~ "Python 3" ]]; then
   	
	sudo apt-get install build-essential cmake pkg-config
	sudo apt-get install libx11-dev libatlas-base-dev
	sudo apt-get install libgtk-3-dev
	sudo apt-get install libboost-all-dev
	sudo apt-get install python3-dev
	sudo pip3 install numpy
    sudo pip3 install opencv-python
	sudo pip3 install dlib
   	sudo pip3 install face_recognition
else 
    echo "Python3 not installed"
fi
