# base = 10
# x = int(input())
# print()
#
# while x > 0:
#     digit = x % base
#     print(digit, end='')
#     x //= base
#


# def read_requests(clients):
#     requests = {}  # Словарь ответов сервера вида {сокет: запрос}
#     for sock in clients:
#         try:
#             data = sock.recv(1024).decode('ascii')
#             requests[sock] = data
#         except:
#             print('Клиент {} {} отключился'.format(sock.fileno(),
#                                                    sock.getpeername()))
#             clients.remove(sock)
#     return requests

class FatherClass:
    def __init__(self, obj):
        self = obj


class SonClass(FatherClass):
    def __init__(self):
        self.a = 'son'
        super().__init__(self)


class DotherClass(FatherClass):
    def __init__(self):
        self.a = 'dother'
        super().__init__(self)

    def __call__(self, *args, **kwargs):
        pass



