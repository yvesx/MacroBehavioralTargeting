#!/home/download/python2.7/bin/python2.7
import web
import process_sentiment


urls = (
    '/test', 'test',
    '/sentence_batch', 'batch'
)
app = web.application(urls, globals())


class test:
    def GET(self):
        process_sentiment.check_JavaGateway()
        return "TESTOK"


class batch:
    def POST(self):
        try:
            return process_sentiment.do(web.data())
        except Exception, e:
            return e


if __name__ == "__main__":
    app.run()
