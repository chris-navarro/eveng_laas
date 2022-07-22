import os, sys

for i in range (0, 10):
    host = '192.168.0.' + str(i)
    conn = os.system('ping -c 1 ' + host + ' > /dev/null')
    
    if conn == 0:
        print(host + ' - Connection Successful')
    else:
        print(host + ' - Connection Failed')
