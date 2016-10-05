from sparrowCTF import *

def pos(g, orig_s, err_s, N):
    r = list(range(1025))
    for x in r:
        if (err_s * pow(g, 2**x, N)) % N == orig_s:
            r.remove(x)
            return x, 1
        elif (orig_s * pow(g, 2**x, N)) % N == err_s:
            r.remove(x)
            return x, 0

def rotate(req):
    req.recv_until(":")
    req.sendline("yes")
    req.recv_until(":")

def NnS():
    r = Remote("192.241.234.35", 31337, debug=False)
    r.sendline("3")
    #get N
    N = r.recvline()[:-1].split(':')[-1]
    rotate(r)
    r.sendline("3")
    #get orig_s
    ss = list()
    while len(ss) == len(set(ss)):
        rotate(r)
        r.sendline("3")
        orig_s = r.recvline().split(',')[0].split(':')[-1]
        ss.append(orig_s)

    return int(N), int(orig_s)

def solve():
    N, orig_s = NnS()
    e = 0x10001
    g = 3
    r = Remote("192.241.234.35", 31337, debug=False)
    res = 0
    bits = 1024
    d = 131811419667704353419669934273801498497646935210532028120447799308664007960357278340261723808572637548407550908403239344903997788296564439667659716110934822412855421586673808904193606481137679044132688115472132575150399986901493501056787817443487153162937855786664238603417924072736209641094219963164897214757
    while bits > -1:
        r.sendline("3")
        sig = int(r.recvline().split(',')[0].split(':')[-1])
        rotate(r)

        if sig == orig_s:
            continue
        p, b = pos(g, orig_s, sig, N)
        res += (2**p) * b
        bits -= 1
        print "[+] {0} bits left to map...\n[+] current d:{1}".format(bits, res)

    assert d == res

def main():
    solve()

if __name__ == "__main__":
    main()
