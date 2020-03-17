#!/bin/bash

echo 'User : ' $PAM_USER $'\n''Service : ' $PAM_SERVICE >> ~/.facelock_logs/logs.log
timeout 120 python3 /etc/facelock/face_unlock.py



