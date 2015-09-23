import socket

target = "127.0.0.1"
target_port = 81

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

client.sendto("AAABBBCCC",(target,target_port))

data,addr = client.recvfrom(4096)

print data