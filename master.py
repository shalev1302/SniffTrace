import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

dat = {}
#172.16.11.8:[ip:(10.0.0.10:20,10.0.0.4:43),port:(80:35,443:245)]
def process_packets(packets,Slaveip):
    global dat
    for ptk in packets:
        if Slaveip in dat:
            if( ptk['ip'] in dat[Slaveip]["ips"]):
                dat[Slaveip]["ips"][ptk['ip']]+=1
            else:
                dat[Slaveip]["ips"][ptk['ip']]=1
            if( ptk['port'] in dat[Slaveip]["ports"]):
                dat[Slaveip]["ports"][ptk['port']]+=1
            else:
                dat[Slaveip]["ports"][ptk['port']]=1
        else:
            dat[Slaveip]={"ips":{ptk["ip"]:1},"ports":{ptk["port"]:1}}

def main():
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(128000)  # buffer size is 1024 bytes
        packets = json.loads(data)
        process_packets(packets,addr[0])
if __name__ == '__main__':
    main()