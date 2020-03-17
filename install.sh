#!/bin/bash

cp -r  ../facelock /etc/
echo 'source /etc/facelock/command.sh' >> ~/.bashrc
if [[  ! -d ~/.facelock_logs ]]; then
    mkdir ~/.facelock_logs/
fi

