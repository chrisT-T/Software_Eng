import asyncio
import threading

import docker
import tornado
import tornado.web
import tornado.websocket

# for RuntimeError: There is no current event loop in thread 'Thread-1'.
loop = asyncio.get_event_loop()


class TerminalForwardingThread(threading.Thread):
    def __init__(self, websocket_handler, terminal_stream):
        super(TerminalForwardingThread, self).__init__(daemon=True)
        self.ws: TerminalSocketHandler = websocket_handler
        self.terminal_stream = terminal_stream

    def run(self):
        asyncio.set_event_loop(loop)
        while True:
            try:
                docker_stream_stdout = self.terminal_stream.recv(2048)
                if len(docker_stream_stdout) == 0:
                    self.ws.close()
                    break
                if docker_stream_stdout is not None:
                    print(docker_stream_stdout)
                    self.ws.write_message(docker_stream_stdout, binary=True)
                else:
                    print("docker daemon socket is close")
                    self.ws.close()
            except Exception as e:
                print("docker daemon socket err: %s" % e)
                self.ws.close()
                break


class TerminalSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, container_id):
        exec_cmd = [
            "/bin/sh",
            "-c",
            '/bin/bash']
        docker_apiclient = docker.APIClient()
        execid = docker_apiclient.exec_create(container_id, exec_cmd, tty=True, stdin=True)
        output = docker_apiclient.exec_start(execid, socket=True, tty=True)._sock

        forwarding_thread = TerminalForwardingThread(self, output)
        forwarding_thread.start()
        self.terminal_socket = output

    def on_message(self, message):
        print("received a message: %s" % (message))
        self.terminal_socket.send(message.encode())

    def on_close(self):
        print("client is closed")

    def check_origin(self, origin):
        return True


app = tornado.web.Application([
    (r"/websocket/(.*)", TerminalSocketHandler)
])

if __name__ == '__main__':
    app.listen(5005)
    tornado.ioloop.IOLoop.instance().start()
