#!/home/download/python2.7/bin/python2.7


class config:
    def __init__(self):

        self.debug        = True
        self.log_critical = '/tmp/pfeclient_critical'
        self.log_message  = '/tmp/pfeclient_message'
        self.log_debug    = '/tmp/pfeclient_debug'

        #self.dbpedia_api = "http://spotlight.dbpedia.org/rest/annotate/"
        self.dbpedia_api = "http://10.1.1.129:9999/rest/annotate/"
        self.wiki_api = "http://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext&exsectionformat=plain&titles="

        self.java_trial = 1
