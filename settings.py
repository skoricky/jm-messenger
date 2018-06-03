import argparse


def get_settings():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, dest="ip", default="", help="host ip")
    parser.add_argument("-p", type=int, dest="port", default=7777, help="port ip")
    parser.add_argument("-s", type=str, dest="status", default="r", help="enabled client status")
    args = parser.parse_args()
    return {"ip": args.ip, "port": args.port, "status": args.status}
