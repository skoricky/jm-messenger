from message import *


def get_message(sock):
    bydata = sock.recv(1024)
    jdata = JMessage().conv_tojson(bydata)
    return jdata


def set_message(sock, action, host=False):
    sock.send(JMessage(action=action, host=host).conv_tobytes())
