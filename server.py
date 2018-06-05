from socket import *
from select import *

from settings import *
from myhost import get_message, set_message


class JServer:
    __listen = 5
    __clients = []

    @property
    def clients(self):
        return self.__clients

    @clients.setter
    def clients(self, value):
        self.__clients = value

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
            # print(f'Server={sock.getsockname()} connection wait...')
            try:
                client, addr = sock.accept()
            except OSError as e:
                pass
            else:
                print(f'Client={addr} connection')
                clients.append(client)
            finally:
                twait = 0
                rclients = []
                wclients = []
                try:
                    rclients, wclients, ex = select(clients, clients, [], twait)
                    print("read: ", rclients)
                    print("write: ", wclients)
                except:
                    pass

                request, clients = JServer.read_requests(rclients)

                clients = JServer.write_responses(wclients)
                # print(f'Server={sock.getsockname()} connection={addr} action={jdata}')
                # client.close() todo: разобраться, когда закрывать клиентов
        sock.close()

    @staticmethod
    def write_responses(clients):
        for sock in clients:
            try:
                set_message(sock, action="probe", host=True)
            except:
                print('Client {} {} down'.format(sock.fileno(),
                                                 sock.getpeername()))
                clients.remove(sock)
        return clients

    @staticmethod
    def read_requests(clients):
        requests = {}
        for sock in clients:
            print(sock)
            try:
                data = get_message(sock)
                requests[sock] = data
                # print("msg: ", requests)
            except:
                print('Client {} {} down'.format(sock.fileno(),
                                                 sock.getpeername()))
                clients.remove(sock)
        return requests, clients


if __name__ == '__main__':
    JServer()
