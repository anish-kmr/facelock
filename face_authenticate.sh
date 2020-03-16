#!/bin/bash

echo "User : " $PAM_USER
echo "Service : "$PAM_SERVICE
timeout 120 python3 /etc/facelock/face_unlock.py



