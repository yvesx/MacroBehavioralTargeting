#!/usr/bin/python
# python io_with_mongo.py some.json

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
