#!/bin/bash

#cd sentiment
#python worker.py "$1" &
/home/download/python2.7/bin/python2.7 worker.py "$@" &
echo $! > /tmp/pfeworker-$1.pid
