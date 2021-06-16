import socket
from scapy.all import sniff
from scapy.layers.inet import IP, Ether
import uuid
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"
Packets = []
SLAVEMAC = (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1]))
PacketsToMaster = []


class packet:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

    def __str__(self):
        return "port:%s ip:%s" % (self.PORT, self.IP)


def main():
    print(SLAVEMAC)
    while True:
        capture = sniff(prn=pkt_callback)


def pktToJson(pkt):
    return {"ip": pkt.IP, "port": pkt.PORT}


def process_pkt(pkt):
    try:
        if (pkt[0].src == SLAVEMAC):
            port = pkt[IP].dport
            ip = pkt[IP].dst

        if (pkt[0].dst == SLAVEMAC):
            port = pkt[IP].sport
            ip = pkt[IP].src
    except IndexError:
        return None

    return packet(ip, port)


def pkt_callback(pkt):
    global Packets
    global PacketsToMaster
    if (pkt[0].src == SLAVEMAC):
        Packets.append(pkt)
    elif (pkt[0].dst == SLAVEMAC):
        Packets.append(pkt)
    else:
        return

    if len(Packets) == 50:  # 50 packets per round
        ports = []
        for pck in Packets:
            procPKT = process_pkt(pck)
            if procPKT is not None:
                PacketsToMaster.append(procPKT)
        test = json.dumps(PacketsToMaster, default=pktToJson)
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)

        sock.sendto(test.encode(), (UDP_IP, 5005))
        PacketsToMaster = []
        Packets = []


if __name__ == '__main__':
    main()
