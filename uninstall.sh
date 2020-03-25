#!/bin/bash


sudo rm -r /etc/facelock

while read -r line
do
  [[ ! $line =~ 'source /etc/facelock/command.sh' ]] && echo "$line"
done < ~/.bashrc > o
sudo mv o ~/.bashrc



