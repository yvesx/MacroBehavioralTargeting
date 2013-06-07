#!/bin/bash
./worker.sh start 1234

curl -XGET http://localhost:1234/test

curl -XPOST http://localhost:1234/sentence_batch -d '[{
"unix_stamp":1284101485,
"text":"Yum, Drumsticks! \"Like\" if you love peanut butter. \"Share\" if you like vanilla peanut butter more. (walmart)"}]'
