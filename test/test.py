import unittest

from settings.settings import *
from chat.message import *


class TestSettings(unittest.TestCase):
    def test_get_settings(self):
        self.assertEqual(tuple(get_settings()), ('', 7777))


class TestServer(unittest.TestCase):
    def test_get_server_sock(self):
        pass


class TestClient(unittest.TestCase):
    def test_get_server_sock(self):
        pass


class TestMessage(unittest.TestCase):
    def test_conv_tobytes(self):
        data = JMessage(action='presence')
        jmsg = json.dumps(data.cli_actions[data.action])
        bymsg = jmsg.encode('utf-8')
        self.assertEqual(data.conv_tobytes(), bymsg)

    def test_conv_tojson(self):
        bymsg = json.dumps('{"json": "True"}').encode('utf-8')
        jmsg = json.loads(bymsg.decode('utf-8'))
        data = JMessage()
        self.assertEqual(data.conv_tojson(bymsg), jmsg)


if __name__ == '__main__':
    unittest.main()
