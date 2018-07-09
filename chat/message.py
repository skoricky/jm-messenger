from datetime import *
import json


def get_message(sock):
    bydata = sock.recv(1024)
    jdata = JMessage().conv_tojson(bydata)
    return jdata


def set_message(sock, action, user="user", host=False):
    sock.send(JMessage(action=action, user=user, host=host).conv_tobytes())


class JMessage:
    __cli_actions = {
        "presence": {
            "action": "presence",
            "time": "",
            "type": "status",
            "user": ""
        },
        "quit": {
            "action": "quit"
        },
        "get_contacts": {
            "action": "get_contacts",
            "time": ""
        },
        "add_contact": {
            "action": "add_contact",
            "user": "",
            "contact": "",
            "time": ""
        },
        "del_contact": {
            "action": "del_contact",
            "user_id": "",
            "time": ""
        }
    }

    __srv_responses = {
        "probe": {
            "action": "probe",
            "time": ""
        },
        "200": {
            "response": "200",
            "time": "",
            "alert": "answer: Ok."
        },
        "202": {
            "response": "202",
            "quantity": ""
        },
        "contact_list": {
            "action": "contact_list",
            "users": {}
        }
    }

    def __init__(self, action=None, user="admin", host=False, encode="utf-8"):
        self.time = datetime.now()
        self.action = action
        self.user = user
        self.host = host
        self.encode = encode

    @property
    def cli_actions(self):
        return self.__cli_actions

    @property
    def srv_responses(self):
        return self.__srv_responses

    def conv_tobytes(self):
        if self.host:
            # self.srv_responses[self.action]["time"] = str(self.time)
            return json.dumps(self.srv_responses[self.action]).encode(self.encode)
        else:
            self.cli_actions[self.action]["user"] = str(self.user)
            if self.action == "add_contact":
                self.cli_actions[self.action]["contact"] = input("Contact name: ")
            return json.dumps(self.cli_actions[self.action]).encode(self.encode)

    def conv_tojson(self, data: bytes):
        return json.loads(data.decode(self.encode))
