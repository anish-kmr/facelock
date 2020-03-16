#!/bin/bash

if [[ "$(python3 -V)" =~ "Python 3" ]]; then
   	sudo pip3 install numpy
    sudo pip3 install opencv-python
	sudo apt-get -y install build-essential cmake libx11-dev git
    cd ~
    mkdir temp
    cd temp
    git clone https://github.com/davisking/dlib.git
    cd dlib
    mkdir build; cd build; cmake ..; cmake --build .
    cd ..
    python3 setup.py install
   	sudo pip3 install face_recognition
else 
    echo "Python3 not installed"
fi
