import datetime

import tornado
import tornado.web
import tornado.websocket

map = {}


class CommunicationSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, projectid, name):
        print(projectid, name)
        self.projectid = projectid
        self.name = name
        map[(projectid, name)] = self
        print(map)

    def on_message(self, message):
        print("received a message: %s" % (message))

        for (projectid, _), client in map.items():
            if projectid == self.projectid:
                client.write_message({"sender": self.name, "msg": message, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    def on_close(self):
        print("closed")
        map.pop((self.projectid, self.name), 0)
        print(map)

    def check_origin(self, origin):
        return True


app = tornado.web.Application([
    (r"/websocket/(.*)/(.*)", CommunicationSocketHandler)
])

if __name__ == '__main__':
    app.listen(6006)
    tornado.ioloop.IOLoop.instance().start()
