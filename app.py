from tornado import websocket, web, ioloop
import json

cl = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class DanmuHandler(web.RequestHandler):
    def get(self):
        self.render("./script/jquery.danmu.js")

class CSSMinHandler(web.RequestHandler):
    def get(self):
        self.render("css/bootstrap.min.css")

class CSSMainHandler(web.RequestHandler):
    def get(self):
        self.render("css/main.css")

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print 'open running now. object:%s' % self
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        print message
        for c in cl:
            c.write_message(json.dumps(message))

    def on_close(self):
        print 'close running now. object:%s' % self
        if self in cl:
            cl.remove(self)

class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id": id, "value" : value}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

    @web.asynchronous
    def post(self):
        pass

app = web.Application([
    (r'/', IndexHandler),
    (r'/danmu.js', DanmuHandler),
    (r'/min.css', CSSMinHandler),
    (r'/main.css', CSSMainHandler),
    (r'/ws', SocketHandler),
    (r'/api', ApiHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
], autoreload=True)

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
