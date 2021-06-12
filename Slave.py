import socket
from scapy.all import *
from scapy.layers.inet import IP,Ether
import uuid

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"
Packets=[]
SLAVEMAC=(':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]))
PacketsToMaster=[]
class packt:
    def __init__(self, IP, PORT):
        self.IP=IP
        self.PORT=PORT

    def __str__(self):
        return  "port:%s ip:%s"% (self.PORT, self.IP)



def main():
    print(SLAVEMAC)
    while True:
        capture = sniff(prn=pkt_callback )


def process_pkt(pkt):
    ip=""
    port=""
    try:
        if(pkt[Ether].src==SLAVEMAC):
            port=pkt[IP].dport
            ip=pkt[IP].dst

        if (pkt[Ether].dst == SLAVEMAC):
            port=pkt[IP].sport
            ip = pkt[IP].src


    except:
        pass

    return packt(ip,port)

def pkt_callback(pkt):
    global Packets
    global PacketsToMaster
    if (pkt[Ether].src == SLAVEMAC):
        Packets.append(pkt)
    elif (pkt[Ether].dst == SLAVEMAC):
        Packets.append(pkt)
    else:
        return


    if(len(Packets)==50): #50 packets per round
        ports=[]
        for pck in Packets:
            PacketsToMaster.append(process_pkt(pck))

        PacketsToMaster=[]
        Packets=[]
if __name__ == '__main__':
    main()