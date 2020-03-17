#!/bin/bash


sudo rm -r /etc/facelock
sudo rm -r ~/.facelock_logs

while read -r line
do
  [[ ! $line =~ 'source /etc/facelock/command.sh' ]] && echo "$line"
done < ~/.bashrc > o
mv o ~/.bashrc



