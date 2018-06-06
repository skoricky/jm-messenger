from socket import *
from select import *
import logging

from settings import *
from myhost import get_message, set_message
import log_config


logger = logging.getLogger('jm.server')


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
        sock.settimeout(0.5)
        logger.info(f'[tcp_server_run]Server={sock.getsockname()} run')
        while True:
            # print(f'Server={sock.getsockname()} connection wait...')
            try:
                client, addr = sock.accept()
            except OSError as e:
                pass
            else:
                logger.info(f'[tcp_server_run]Client={addr} connection')
                # print(f'Client={addr} connection')
                clients.append(client)
            finally:
                rclients, wclients = JServer.get_select_clients(clients)
                request, clients = JServer.read_requests(rclients)
                clients = JServer.write_responses(request, wclients)
                # print(f'Server={sock.getsockname()} connection={addr} action={jdata}')
                # client.close() todo: разобраться, когда закрывать клиентов
        sock.close()

    @staticmethod
    def get_select_clients(clients):
        twait = 0
        rclients = []
        wclients = []
        try:
            rclients, wclients, ex = select(clients, clients, [], twait)
            if len(rclients) > 0:
                logger.debug(f'[get_select_clients]clients read: {rclients}')
                print("read: ", rclients)
            if len(wclients) > 0:
                logger.debug(f'[get_select_clients]clients write: {wclients}')
                print("write: ", wclients)
        except:
            pass
            # logger.debug(f'clients no select')
            # print(f'clients no select')
        return rclients, wclients

    @staticmethod
    def write_responses(requests, clients):
        for sock in clients:
            for _ in requests:
                try:
                    data = requests[_]
                    set_message(sock, action=data["action"])
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
