from datetime import *
import json


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
            self.srv_responses[self.action]["time"] = str(self.time)
            return json.dumps(self.srv_responses[self.action]).encode(self.encode)
        else:
            self.cli_actions[self.action]["time"] = str(self.time)
            return json.dumps(self.cli_actions[self.action]).encode(self.encode)

    def conv_tojson(self, data: bytes):
        return json.loads(data.decode(self.encode))

    # def send_message(self):
    #     self.sock.send(self.conv_tobytes())
    #
    # def recv_message(self, bydata):
    #     return self.conv_tojson(bydata)
