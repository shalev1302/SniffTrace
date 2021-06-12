import os

netstat = os.popen("netstat -nb")
netstat_str = netstat.read()
print(netstat_str)