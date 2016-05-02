import webapp2
import struct
import base64
from flag import FLAG

def jekyll32(data, seed):
    def mix(a, b, c):
        a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

        a -= b+c; a &= 0xFFFFFFFF; a ^= c >> 13
        b -= c+a; b &= 0xFFFFFFFF; b ^=(a <<  8)&0xFFFFFFFF
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 13
        a -= b+c; a &= 0xFFFFFFFF; a ^= c >> 12
        b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 16)&0xFFFFFFFF
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >>  5
        a -= b+c; a &= 0xFFFFFFFF; a ^= c >>  3
        b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 10)&0xFFFFFFFF
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 15

        return a, b, c

    a = 0x9e3779b9
    b = a
    c = seed
    length = len(data)

    keylen = length
    while keylen >= 12:
        values = struct.unpack('<3I', data[:12])
        a += values[0]
        b += values[1]
        c += values[2]

        a, b, c = mix(a, b, c)
        keylen -= 12
        data = data[12:]

    c += length

    data += '\x00' * (12-len(data))
    values = struct.unpack('<3I', data)

    a += values[0]
    b += values[1]
    c += values[2]

    a, b, c = mix(a, b, c)

    return c

def jekyll(data):
    return jekyll32(data, 0x60061e) | (jekyll32(data, 0x900913) << 32)

class AdminPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        cookie = self.request.cookies.get('admin')

        if cookie is not None and jekyll(base64.b64decode(cookie)) == 0x203b1b70cb122e29:
            self.response.write('Hello admin!\n'+FLAG)
        else:
            self.response.write('Who are you?')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', AdminPage),
], debug=False)

