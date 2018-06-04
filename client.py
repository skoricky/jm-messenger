from socket import *

from settings import *
from message import *


class JClient:

    def __init__(self):
        host_settings = get_settings()
        self.sock = self.get_client_sock()
        self.tcp_client_run(self.sock, (host_settings["ip"], host_settings["port"]))

    @staticmethod
    def get_client_sock(sock_type=SOCK_STREAM):
        sock = socket(AF_INET, sock_type)
        return sock

    @staticmethod
    def tcp_client_run(sock, host_settings):
        sock.connect(host_settings)
        sock.send(JMessage(action="presence").conv_tobytes())
        bydata = sock.recv(1024)
        if bydata:
            jdata = JMessage().conv_tojson(bydata)
            print(f'Server={host_settings} response={jdata}')
        sock.send(JMessage(action="quit").conv_tobytes())
        sock.close()


if __name__ == '__main__':
    JClient()