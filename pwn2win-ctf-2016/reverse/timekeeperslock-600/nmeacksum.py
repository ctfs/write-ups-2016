#!/usr/bin/python3
import sys, re
from functools import reduce

def cksum(s):
    return '%02X' % reduce(lambda a,b:a^b, map(ord, s))

def cksum_all(s):
    for m in re.finditer(r'\$([^*]+)\*', s):
        yield m.group(0) + cksum(m.group(1))

if __name__ == '__main__':
    if len(sys.argv) != 2 or (len(sys.argv) > 1 and sys.argv[1] == '-h'):
        sys.stderr.write("usage: %s 'nmea_string'\n" % sys.argv[0])
        sys.exit(1)
    print(''.join(cksum_all(sys.argv[1])))
