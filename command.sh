#!/bin/bash


function facelock(){
    export QT_X11_NO_MITSHM=1
    sudo /home/chandan/anaconda3/bin/python3 /etc/facelock/main.py $@
}