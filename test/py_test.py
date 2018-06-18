import socket

from chat.message import *


class Mysocket:
    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        self.data = b''
        self.setting = ()

    def send(self, data):
        self.data = data
        return len(data)

    def recv(self, n):
        return JMessage(action='presence', host=False).conv_tobytes()

    def dind(self, setting):
        self.setting = setting


def test_send_data(monkeypatch):
    monkeypatch.setattr("socket.socket", Mysocket)
    sock = socket.socket()
    set_message(sock, 'presence')
    assert sock.data == JMessage(action='presence', host=False).conv_tobytes()


def test_recv_data(monkeypatch):
    monkeypatch.setattr("socket.socket", Mysocket)
    sock = socket.socket()
    jdata = get_message(sock)
    bydata = JMessage(action='presence', host=False).conv_tobytes()
    assert jdata == JMessage().conv_tojson(bydata)

