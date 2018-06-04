# base = 10
# x = int(input())
# print()
#
# while x > 0:
#     digit = x % base
#     print(digit, end='')
#     x //= base
#


def read_requests(clients):
    requests = {}  # Словарь ответов сервера вида {сокет: запрос}
    for sock in clients:
        try:
            data = sock.recv(1024).decode('ascii')
            requests[sock] = data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(),
                                                   sock.getpeername()))
            clients.remove(sock)
    return requests
