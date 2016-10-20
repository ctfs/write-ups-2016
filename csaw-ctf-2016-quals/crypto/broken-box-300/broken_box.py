from functools import wraps
import errno
import os
import signal
import SocketServer
import random, time

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

@timeout(60)
def recv(req, bytes):
        return req.recv(bytes)

def sign(req):
        d = 131811419667704353419669934273801498497646935210532028120447799308664007960357278340261723808572637548407550908403239344903997788296564439667659716110934822412855421586673808904193606481137679044132688115472132575150399986901493501056787817443487153162937855786664238603417924072736209641094219963164897214757
        N = 172794691472052891606123026873804908828041669691609575879218839103312725575539274510146072314972595103514205266417760425399021924101213043476074946787797027000946594352073829975780001500365774553488470967261307428366461433441594196630494834260653022238045540839300190444686046016894356383749066966416917513737
        bits = list(range(0, 1025))
        random.shuffle(bits)
        while True:
            req.sendall("Input an number(0~9999) to be signed:")
            msg = recv(req, 5)
            try:
                g = int(msg)
                if g < 0 or g > 9999:
                        raise Exception
            except:
                req.sendall("Wrong input, quitting...")
                return

            if random.random() < 0.5:
                pos = bits.pop()
                enc = pow(g, d^(2**pos), N)
            else:
                enc = pow(g, d, N)
            req.sendall("signature:{0}, N:{1}".format(str(enc), N))
            req.sendall("\nSign more items?(yes, no):")
            choice = recv(req, 4).split('\n')[0]
            if choice == 'no':
                break

class incoming(SocketServer.BaseRequestHandler):
    def handle(self):
        random.seed(time.time())
        req = self.request
        sign(req)

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass

SocketServer.TCPServer.allow_reuse_address = True
server = ReusableTCPServer(("0.0.0.0", 8000), incoming)
server.timeout = 60
server.serve_forever()
