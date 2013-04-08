import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import random
import tornado.template


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", name = "Bogdan")
    def write_error(self, status_code, **kwargs):
        self.write("No method to handle request. Error code %d." %status_code)

class HelloHandler(tornado.web.RequestHandler):
    def get(self, name):
        self.render("index.html", name = name)
def write_error(self, status_code, **kwargs):
    self.write("No method to handle request. Error code %d." %status_code)

if __name__ == "__main__":

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler), (r"/(\w+)", HelloHandler)],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"))
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port);
    tornado.ioloop.IOLoop.instance().start()