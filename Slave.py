import socket
from scapy.all import *
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"
Packets=[]
def main():
    while True:
        capture = sniff(prn=pkt_callback )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
def pkt_callback(pkt):
    global Packets
    Packets.append(pkt)
    if(len(Packets)==50): #50 packets per round 
        print("send")
        Packets=[]
if __name__ == '__main__':
    main()