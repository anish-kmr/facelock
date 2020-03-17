#!/bin/bash

cp -r  ../facelock /etc/
echo 'source /etc/facelock/command.sh' >> ~/.bashrc
mkdir ~/.facelock_logs/
