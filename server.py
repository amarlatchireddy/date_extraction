import tornado.ioloop
import tornado.web
from dateextract import process
import json

class Extract(tornado.web.RequestHandler):

    def post(self):
        print(self.request.body.decode('utf-8'))
        inputJson = json.loads(self.request.body.decode('utf-8'))
        # print(inputJson['base_64_image_content'])
        resultDate = process(inputJson['base_64_image_content'])
        resJson = {
            'date': resultDate
        }
        self.write(json.dumps(resJson))

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/extract_date", Extract)
    ])
    application.listen(9002)
    tornado.ioloop.IOLoop.instance().start()