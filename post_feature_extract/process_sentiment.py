#!/home/download/python2.7/bin/python2.7

import urllib
import urllib2
import HTMLParser
import sys
import json
import re
import os
import time
from datetime import datetime
from nltk.tokenize import word_tokenize
from guess_language import guess_language
import conf
import error
import dictionary
from py4j.java_gateway import JavaGateway

config = conf.config()
dict_hash = {}
# port for POS tagger
port = 25333
app = None


def init():
    add_dict('zh', './keyword_list/keyword_list_cn/')
    add_dict('en', './keyword_list/keyword_list_en/')
    add_dict('fr', './keyword_list/keyword_list_fr/')
    add_dict('ge', './keyword_list/keyword_list_ge/')
    add_dict('kr', './keyword_list/keyword_list_kr/')
    add_dict('po', './keyword_list/keyword_list_po/')
    add_dict('ro', './keyword_list/keyword_list_ro/')
    add_dict('sp', './keyword_list/keyword_list_sp/')


def add_dict(language, path):
    dict_hash[language] = dictionary.Dictionary(language, path)


def process( unix_stamp, sentence):
    lang = guess_language(sentence).lower()
    #lang = 'en'
    if lang in dict_hash:
        dict_match = dict_hash[lang]
    else:
        dict_match = dict_hash['en']

    sentence_orig_case = sentence.encode('utf-8')
    array = tokenize_word(dict_match, sentence_orig_case)

    #detect if contains an upper case word
    contains_upper_case = 0
    for word in array:
        if all(char.isupper() for char in word):
            contains_upper_case = 1
            break

    sentence = sentence.lower().encode('utf-8')

    #detect if contains a:
    # question
    # exclamation
    # a hashtag
    # a url
    # if ask to like
    # if ask to share
    # long piece of text
    # name entities from wikification
    # list of pos/neg words
    reg = re.compile('.*(what|why|how|when|where).*\?$')
    if reg.match(sentence) is not None:
        question = 1
    else:
        question = 0

    if '!' in sentence:
        exclamation = 1
    else:
        exclamation = 0

    if '#' in sentence:
        hash_tag = 1
    else:
        hash_tag = 0

    if 'http' in sentence:
        hyper_link = 1
    else:
        hyper_link = 0

    if len(sentence) > 140:
        long_text = 1
    else:
        long_text = 0

    name_entities = wikification(sentence)
    array = tokenize_word(dict_match, sentence)

    negations = [w for w in array if w in dict_match.negation_hash]
    positives = [w for w in array if w in dict_match.pos_word_hash]
    negatives = [w for w in array if w in dict_match.neg_word_hash]
    POS = POS_tag(sentence_orig_case)

    ask_like = 0
    ask_share = 0
    for part in POS:
        if part['pos'] == "V":
            if part['word'].lower() == "like":
                ask_like = 1
            elif part['word'].lower() == "share":
                ask_share = 1


    HOD = datetime.fromtimestamp(unix_stamp).hour
    MOY = datetime.fromtimestamp(unix_stamp).month
    DOW = datetime.fromtimestamp(unix_stamp).isoweekday()
    result = {"language":lang,
              "contains_upper_case":contains_upper_case,
              "question":question,
              "exclamation":exclamation,
              "hash_tag":hash_tag,
              "hyper_link":hyper_link,
              "ask_like":ask_like,
              "ask_share":ask_share,
              "long_text":long_text,
              "name_entities":name_entities,
              "negations":negations,
              "positives":positives,
              "negatives":negatives,
              "POS":POS,
              "HOD":HOD,
              "MOY":MOY,
              "DOW":DOW
             }
    return result


def tokenize_word(dict_match, sentence):
    array = word_tokenize(sentence)
    #word correction
    for idx, val in enumerate(array):
        if val in dict_match.correction_hash:
            array[idx] = dict_match.correction_hash[val]

    return array


def wikification(text):
    array = []
    values = {
        "text": text,
        "confidence": 0.0,
        "support": 0,
        "spotter": "CoOccurrenceBasedSelector",
        "disambiguator": "Document"
    }
    data = urllib.urlencode(values)
    headers = {"Accept": "application/json", "content-type": "application/x-www-form-urlencoded"}
    req = urllib2.Request(config.dbpedia_api, data, headers)
    try:
        result = urllib2.urlopen(req, timeout=60).read()
        json_data = json.loads(result)

    except Exception, e:
        error.write_log(str(e) + " Can't get dbpedia result", 1)
        return None

    if 'Resources' in json_data:
        for item in json_data['Resources']:
            array.append(item)
    return array


def POS_tag(text):
    try:
        return json.loads(app.runTagger(text))
    except Exception:
        error.write_log("Error in connecting to the Java Gateway", 1)
        return []



def do(data_str):
    result = []

    try:
        data = json.loads(data_str)
    except Exception:
        error.write_log("Bad Syntax in the input", 1)
        return "ERROR! Bad Syntax in the input"

    for item in data:
        if 'text' in item.keys() and 'unix_stamp' in item.keys():
            result.append( dict( item.items() + process(item['unix_stamp'], item['text']).items() ) )

    return json.dumps(result)


def restart_JavaGateway():
    os.system("ssh localhost \"~/sc/sentiment/tagger.sh restart " + str(port) + " \" &")
    #time.sleep(5)


def check_JavaGateway():
    try:
        global app
        app = JavaGateway(python_proxy_port=port).entry_point

        if app.test() != "TESTOK":
            restart_JavaGateway()

    except Exception:
        restart_JavaGateway()


init()
check_JavaGateway()


def main():
    print do(sys.argv[1], False)

if __name__ == '__main__':
    main()
