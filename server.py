from socket import *
from select import *

from settings import *
from message import *


class JServer:
    __listen = 5
    __clients = []

    @property
    def clients(self):
        return self.__clients

    @clients.setter
    def clients(self, value):
        self.__clients.append(value)

    @property
    def listen(self):
        return self.__listen

    def __init__(self):
        host_settings = get_settings()
        self.sock = self.get_server_sock((host_settings["ip"], host_settings["port"]))
        self.tcp_server_run(self.sock, self.listen, self.clients)

    @staticmethod
    def get_server_sock(host_settings, sock_type=SOCK_STREAM):
        sock = socket(AF_INET, sock_type)
        sock.bind(host_settings)
        return sock

    @staticmethod
    def tcp_server_run(sock, listen, clients):
        sock.listen(listen)
        sock.settimeout(0.2)
        while True:
            print(f'Server={sock.getsockname()} connection wait...')
            try:
                client, addr = sock.accept()
            except:
                pass
            else:
                print(f'Client={addr} connection')
                clients(client)
            finally:
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select(clients, clients, [], wait)
                except:
                    pass

            while True:
                bydata = client.recv(1024)
                if not bydata:
                    break
                jdata = JMessage().conv_tojson(bydata)
                if jdata["action"] != "quit":
                    client.send(JMessage(action="200", host=True).conv_tobytes())
                print(f'Server={sock.getsockname()} connection={addr} action={jdata}')
            client.close()
        sock.close()

    def get_message(self, sock):
        bydata = sock.recv(1024)
        jdata = JMessage().conv_tojson(bydata)
        return jdata

    def set_message(self, sock):
        pass

    def write_responses(self, response, clients):
        pass

    def read_requests(self, clients):
        requests = {}
        for sock in clients:
            try:
                data = self.get_message(sock)
                requests[sock] = data
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(),
                                                       sock.getpeername()))
                clients.remove(sock)
        return requests


if __name__ == '__main__':
    JServer()
