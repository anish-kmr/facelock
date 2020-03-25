#!/bin/bash


function facelock(){
    export QT_X11_NO_MITSHM=1
    sudo python3 /etc/facelock/main.py $@
}
