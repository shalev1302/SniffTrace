import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

dat = {}
i = 3

def load_data():
    global dat
    with open('data.json', 'r') as f:
        dat = json.load(f)


def export_data():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(dat, f, ensure_ascii=False, indent=4)


def process_packets(packets, Slaveip):
    global dat
    for ptk in packets:
        if Slaveip in dat:
            if ptk['ip'] in dat[Slaveip]["ips"]:
                dat[Slaveip]["ips"][ptk['ip']] += 1
            else:
                dat[Slaveip]["ips"][ptk['ip']] = 1
            if ptk['port'] in dat[Slaveip]["ports"]:
                dat[Slaveip]["ports"][ptk['port']] += 1
            else:
                dat[Slaveip]["ports"][ptk['port']] = 1
        else:
            dat[Slaveip] = {"ips": {ptk["ip"]: 1}, "ports": {ptk["port"]: 1}}
    export_data()


def main():
    global dat
    load_data()
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, adder = sock.recvfrom(128000)  # buffer size is 1024 bytes
        packets = json.loads(data)
        process_packets(packets, adder[0])


if __name__ == '__main__':
    main()
