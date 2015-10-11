# coding=utf-8
import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import sys
import logging
import json
from tornado.options import define, options

reload(sys)
sys.setdefaultencoding('utf-8')
define("port", default=8002, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class ContentHandler(tornado.web.RequestHandler):
    def get(self, input):
        filename = input + ".json"
        logging.info(filename)
        fileobj = open(filename, "r")
        content = fileobj.read()
        self.write(content)

class ClassInfoHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        time = data[0]['time']
        name = data[0]['student']
        filename = "classinfo\\" + time + name + ".json"
        fileobj = open(filename, "w")
        fileobj.write(json.dumps(data))

class ClassListHandler(tornado.web.RequestHandler):
    def get(self):
        list = []
        url = []
        for root,dirs,files in os.walk("classinfo/"):
            for name in files:
                list.append(name.decode('GBK'))
                url.append("classdetail/"+name.decode('GBK'))
        self.render("allclass.html",info=list,classurl=url)

class ClassDetailHandler(tornado.web.RequestHandler):
    def get(self,input):
        filename = "classinfo/"+input
        fileobj = open(filename, "r")
        content = fileobj.read()
        classinfo = json.loads(content)
        time = classinfo[0]['time']
        name = classinfo[0]['student']
        self.render("classinfo.html", info=classinfo)

class Application(tornado.web.Application):
    def __init__(self):
        csspath = os.path.join(os.path.dirname(__file__), "css")
        jspath = os.path.join(os.path.dirname(__file__), "js")
        fontpath = os.path.join(os.path.dirname(__file__), "fonts")
        handlers = [(r"/", MainHandler),
                    (r"/content(\w+)", ContentHandler),
                    (r"/classinfo", ClassInfoHandler),
                    (r"/classlist", ClassListHandler),
                    (r"/classdetail", ClassDetailHandler),
                    (r'/fonts/(.*)', tornado.web.StaticFileHandler, {'path': fontpath}),
                    (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': jspath}),
                    (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': csspath})]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
