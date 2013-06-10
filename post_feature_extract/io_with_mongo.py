#!/usr/bin/python
# python ./fire_requests.py 309506851302 > bmw.json# bmw
# python ./fire_requests.py 134615383218473 > bk.json# BK
# python ./fire_requests.py 7224956785 > samsung.json # samsung mobile
# python ./fire_requests.py 211718455520845 > visa.json # visa

import sys
import os
import string
import time
import config
import json


config = config.config()
mongo_collection = config.mongo_collection

json_data=open(sys.argv[1])

array = json.load(json_data)
mongo_collection = config.mongo_collection
mongo_collection.insert(array,continue_on_error=True)
