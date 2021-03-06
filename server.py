from socket import *
from select import *
import logging

from settings.settings import *
from chat.message import get_message, set_message
from log.log_config import *
from repository.repository import create_repository

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
        self.session = create_repository()
        self.tcp_server_run(self.sock, self.listen, self.clients, self.session)

    @staticmethod
    def get_server_sock(host_settings, sock_type=SOCK_STREAM):
        sock = socket(AF_INET, sock_type)
        sock.bind(host_settings)
        return sock

    @staticmethod
    def tcp_server_run(sock, listen, clients, session=None):
        sock.listen(listen)
        sock.settimeout(0.5)
        logger.info(f'[tcp_server_run]Server={sock.getsockname()} run')
        while True:
            try:
                client, addr = sock.accept()
            except OSError as e:
                pass
            else:
                logger.info(f'[tcp_server_run]Client={addr} connection')
                print(f'Client={addr} connection')
                clients.append(client)
                # session.session.close()
            finally:
                rclients, wclients = JServer.get_select_clients(clients)
                request, clients = JServer.read_requests(rclients, clients, session)
                clients = JServer.write_responses(request, wclients, clients)
        sock.close()

    @staticmethod
    def get_select_clients(clients):
        twait = 0
        rclients = []
        wclients = []
        try:
            rclients, wclients, ex = select(clients, clients, [], twait)
            if len(rclients) > 0:
                logger.debug(f'[get_select_clients]server read: {rclients}')
                print("read: ", rclients)
            if len(wclients) > 0:
                logger.debug(f'[get_select_clients]server write: {wclients}')
                print("write: ", wclients)
        except:
            pass
        return rclients, wclients

    @staticmethod
    def write_responses(request, wclients, clients):
        for sock in wclients and clients:
            for _ in request:
                try:
                    data = request[_]
                    # set_message(sock, action=data["action"], user=data["user"])
                except:
                    logger.info(f'[get_select_clients]Client {sock.fileno()} {sock.getpeername()} down')
                    print('Client {} {} down'.format(sock.fileno(),
                                                     sock.getpeername()))
                    clients.remove(sock)
        return clients

    @staticmethod
    def read_requests(rclients, clients, session):
        requests = {}
        for sock in rclients:
            try:
                data = get_message(sock)
                requests[sock] = data
                logger.debug(f'[get_select_clients]Client={sock.fileno()}{sock.getpeername()} action: {data}')
                print("msg: ", f'Client={sock.fileno()}{sock.getpeername()} action: {data}')
                session.add_client(data["user"])
                if data["action"] == "presence":
                    session.add_session(f'{addr[0]} {addr[1]}')
                if data["action"] == "add_contact":
                    session.add_contact(data["user"], data["contact"])
            except:
                logger.info(f'[get_select_clients]Client {sock.fileno()} {sock.getpeername()} down')
                print('Client {} {} down'.format(sock.fileno(),
                                                 sock.getpeername()))
                clients.remove(sock)
        return requests, clients

    def commit_session(self, data):
        pass


if __name__ == '__main__':
    JServer()
