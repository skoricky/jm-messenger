from socket import *

from settings import *
from message import *


class JServer:
    __listen = 5

    @property
    def listen(self):
        return self.__listen

    def __init__(self):
        self.sock = self.get_server_sock(tuple(get_settings()))
        self.tcp_server_run(self.sock, self.listen)

    def get_server_sock(self, host_settings, sock_type=SOCK_STREAM):
        sock = socket(AF_INET, sock_type)
        sock.bind(host_settings)
        return sock

    def tcp_server_run(self, sock, listen):
        sock.listen(listen)
        while True:
            print(f'Server={sock.getsockname()} connection wait...')
            client, addr = sock.accept()
            while True:
                bydata = client.recv(1024)
                if not bydata:
                    break
                jdata = JMessage(host=True).conv_tojson(bydata)
                if jdata["action"] != "quit":
                    client.send(JMessage(action="200", host=True).conv_tobytes())
                print(f'Server={sock.getsockname()} connection={addr} action={jdata}')
            client.close()
        sock.close()


if __name__ == '__main__':
    JServer()
