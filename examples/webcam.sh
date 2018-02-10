#!/usr/bin/env bash

DATE=$(date +"%Y-%m-%d_%H%M")

mkdir -p ~/webcam
fswebcam -r 1280x720 ~/webcam/$DATE.jpg
