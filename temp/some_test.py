_list = [2, 4, 4, 3, 3]


def find_number(some_list):
    xor_sum = 0
    for i in some_list:
        xor_sum = xor_sum ^ i
        # print(xor_sum)
    return xor_sum


if __name__ == '__main__':
    print(find_number(_list))
