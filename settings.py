import argparse


def get_settings():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, dest="ip", default="", help="host ip")
    parser.add_argument("-p", type=int, dest="port", default=7777, help="port ip")
    args = parser.parse_args()
    return args.ip, args.port
