from socket import *
import time

from settings import *
from myhost import get_message, set_message


class JClient:

    def __init__(self):
        host_settings = get_settings()
        self.sock = self.get_client_sock()
        self.tcp_client_run(self.sock, (host_settings["ip"], host_settings["port"]), host_settings["status"])

    @staticmethod
    def get_client_sock(sock_type=SOCK_STREAM):
        sock = socket(AF_INET, sock_type)
        return sock

    @staticmethod
    def tcp_client_run(sock, host_settings, status):
        flag = True
        sock.connect(host_settings)
        while True:
            if status == 'r':
                data = get_message(sock)
                if data:
                    print(f'Server={host_settings} response={data}')
            else:
                if flag:
                    flag = False
                    set_message(sock, action="presence")
                else:
                    action = input('action= ')
                    if action[0].lower() == 'q':
                        set_message(sock, action="quit")
                        time.sleep(0.2)
                        break
                    else:
                        set_message(sock, action)
        sock.close()



if __name__ == '__main__':
    JClient()