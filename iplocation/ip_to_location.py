#!/usr/bin/env python
#fileencoding=utf-8

import struct
import socket


class Node(object):
    __slots__ = ('ip', 'country', 'district')

    def __init__(self, ip, country, district):
        self.ip = ip
        self.country = country
        self.district = district

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'IPRecord(ip: {}; country: {}; district: {})'.format(
            socket.inet_ntoa(struct.pack("!L", self.ip)),
            self.country, self.district)


def parse_long_4(bytes_):
    return struct.unpack('<L', bytes_)[0]


def parse_long_3(bytes_):
    return struct.unpack('<L', bytes_ + '\x00')[0]


def parse_char(bytes_):
    return struct.unpack('<b', bytes_)[0]


def read_c_string(data, begin):
    end = begin
    while data[end] != '\x00':
        end += 1
    # exclude trailing \0
    return data[begin: end].decode('gbk', 'replace'), end + 1


def read_string(data, begin):
    mode = parse_char(data[begin: begin + 1])
    if mode == 2:
        offset = parse_long_3(data[begin + 1: begin + 4])
        return read_c_string(data, offset)[0], begin + 4
    else:
        return read_c_string(data, begin)


def parse_record(data, begin):
    ip = parse_long_4(data[begin: begin + 4])
    mode = parse_char(data[begin + 4: begin + 5])
    begin = begin + 5
    if mode == 1:
        record_begin = parse_long_3(data[begin: begin + 3])
        country, record_begin = read_string(data, record_begin)
        district, _ = read_string(data, record_begin)
    elif mode == 2:
        begin -= 1
        country, record_begin = read_string(data, begin)
        district, _ = read_string(data, record_begin)
    else:
        begin -= 1
        country, record_begin = read_c_string(data, begin)
        district, _ = read_string(data, record_begin)
    return Node(ip, country, district)


def parse(data):
    ips = []
    index_offset_first, index_offset_last = \
        parse_long_4(data[0: 4]), parse_long_4(data[4: 8])
    while index_offset_first <= index_offset_last:
        record = parse_record(data, parse_long_3(
            data[index_offset_first + 4: index_offset_first + 7]))
        ips.append(record)
        index_offset_first += 7
    return ips


class IP2Location(object):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            self.ips = parse(f.read())
        for ip in self.ips:
            if ip.district == u' CZ88.NET':
                ip.district = u''
        if self.ips[-1].ip == 0xffffffffL:
            self.ips[-1].country = u'IANA保留地址'
            self.ips[-1].district = u''

    def get_location(self, ip):
        if isinstance(ip, str):
            ip = struct.unpack('!L', socket.inet_aton(ip))[0]
        ips = self.ips
        low = 0
        len_ = len(ips)
        # lower_bound
        while len_ > 0:
            half_len = len_ / 2
            mid = low + half_len
            if ips[mid].ip < ip:
                low = mid + 1
                len_ = len_ - half_len - 1
            else:
                len_ = half_len
        assert low < len(ips)
        return ips[low]


class IP2LocationMe(object):
    '''
    memory efficient
    '''
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            self.data = f.read()
        self.index_begin, index_end = \
            parse_long_4(self.data[0: 4]), parse_long_4(self.data[4: 8]) + 7
        self.index_len = (index_end - self.index_begin) / 7

    def get_location(self, ip):
        if isinstance(ip, str):
            ip = struct.unpack('!L', socket.inet_aton(ip))[0]

        data = self.data
        low = self.index_begin
        len_ = self.index_len
        # lower_bound
        while len_ > 0:
            half_len = len_ / 2
            mid = low + half_len * 7
            offset = parse_long_3(data[mid + 4: mid + 7])
            mid_ip = parse_long_4(data[offset: offset + 4])
            if mid_ip < ip:
                low = mid + 7
                len_ = len_ - half_len - 1
            else:
                len_ = half_len

        record = parse_record(data, parse_long_3(
            data[low + 4: low + 7]))
        if record.district == u' CZ88.NET':
            record.district = u''
        if record.ip == 0xffffffff:
            record.country = u'IANA保留地址'
            record.district = u''
        return record


def get_location(ip):
    import os
    self_dir = os.path.dirname(os.path.abspath(__file__))
    client = IP2LocationMe(os.path.join(self_dir, 'ip_to_location.dat'))
    globals()['get_location'] = client.get_location
    return client.get_location(ip)


def main():
    try:
        while True:
            ip = raw_input('ip:')
            loc = get_location(ip)
            print hex(loc.ip), loc.country, loc.district
    except EOFError:
        pass


if __name__ == '__main__':
    main()
