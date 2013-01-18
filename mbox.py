import mailbox
from collections import defaultdict
import socket

import re
# Credit: http://answers.oreilly.com/topic/318-how-to-match-ipv4-addresses-with-regular-expressions/
ip_re = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

def ip_string_to_int(ip_string):
    octets = map(int, ip_string.split('.'))
    assert len(octets) == 4
    ip_address = 0
    for i, octet in enumerate(reversed(octets)):
        ip_address = ip_address | (octet << i*8)
    return ip_address

def ip_int_to_string(ip_int):
    assert ip_int >= 0
    octets = []
    for i in reversed(xrange(4)):
        octets.append((ip_int & (255 << i*8)) >> i*8)
    return '.'.join(map(str, octets))

def is_private_ip(ipaddr):
    """
    http://tools.ietf.org/html/rfc1918
    """
    private_ip_ranges = (
            ('10.0.0.0', '10.255.255.255'),
            ('127.0.0.0', '127.255.255.255'),
            ('172.16.0.0', '172.31.255.255'),
            ('192.168.0.0', '192.168.255.255')
        )
    ip = ip_string_to_int(ipaddr)
    for ip_range in private_ip_ranges:
        ip_range_start, ip_range_end = map(ip_string_to_int, ip_range)
        if ip_range_start <= ip <= ip_range_end:
            return True
    return False

def is_public_ip(ip):
    return not is_private_ip(ip)

def get_reverse_dns(ip):
    # TODO: would be nice to make this threaded for performance
    # interesting: http://docs.python.org/2/howto/sockets.html
    try:
        if hasattr(socket, 'setdefaulttimeout'):
            socket.setdefaulttimeout(5)
        return socket.gethostbyaddr(ip)
    except socket.herror:
        pass

def get_source_ip(message):
    # From docs: "in a Message object, headers are always returned in the order
    # they appeared in the original message"

    # Logic:
    # 1. use X-Originating-IP, if found
    # 2. use earliest (appended, latest in appearance) received IP
    #    that has a public ip

    source_header = None
    if message.has_key('X-Originating-IP'):
        source_header = message['X-Originating-IP']
    else:
        for received_header in reversed(message.get_all('Received')):
            recv_ip = None
            try:
                recv_ip = re.search(ip_re, received_header).group()
            except:
                continue
            if is_public_ip(recv_ip):
                source_header = received_header
                break
    return re.search(ip_re, source_header).group()

mbox = mailbox.mbox("mini.mbox")

# test finding "best" ip from a message
#firstmsg = mbox.values()[0]
#for k, v in firstmsg.items():
#    print k, ":", v
#print get_source_ip(firstmsg)

# build a dictionary of metadata for each IP
# for each From: address, I want a list of (IP, timestamp)
ip_metadata = defaultdict(list)

for msg in mbox.itervalues():
    #print msg['From']
    source_ip = get_source_ip(msg)
    ip_metadata[msg['From']].append((
        source_ip,
        get_reverse_dns(source_ip),
        msg['Date']
    ))

print ip_metadata
