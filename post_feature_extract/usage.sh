#!/bin/bash
./worker.sh start 1234

curl -XGET http://localhost:1234/test

curl -XPOST http://localhost:1234/sentence_batch -d '[{"unix_stamp":1284101485, "text":"Yum, Drumsticks! Like if you love peanut butter. Share if you like vanilla peanut butter more. (walmart)"}]'

# OR

# on guru mysql
python fire_requests.py 14408401557 > kindle.json
# on social server
curl -XPOST http://localhost:1234/sentence_batch --data @kindle.json > kindle_out.json
# on mongo
python io_with_mongo.py some.json


# for post similarity
python get_post_similarity.py 309506851302 bmw_post_sim.json&
python get_post_similarity.py 134615383218473 bk_post_sim.json&
python get_post_similarity.py 7224956785 samsung_post_sim.json&
python get_post_similarity.py 211718455520845 visa_post_sim.json&

python get_post_similarity.py put bmw_post_sim.json&
python get_post_similarity.py put bk_post_sim.json
python get_post_similarity.py put samsung_post_sim.json
python get_post_similarity.py put visa_post_sim.json

