from flag import FLAG
FLAG = int(FLAG.encode('hex'),16)

P = 0xd3ceec4c84af8fa5f3e9af91e00cabacaaaecec3da619400e29a25abececfdc9bd678e2708a58acb1bd15370acc39c596807dab6229dca11fd3a217510258d1b
A = 0x95fc77eb3119991a0022168c83eee7178e6c3eeaf75e0fdf1853b8ef4cb97a9058c271ee193b8b27938a07052f918c35eccb027b0b168b4e2566b247b91dc07
Gx = 0xcf634030986cf41c1add87e71d638b9cc723c764059cf4c9b8ed2a0aaf5d51dc770372503ebfaad746ab9220e992c09822916978226465ad31d354a3efee51da
Gy = 0x65eaad8848b2787103fce02358b45d8a61420031989eb6b4b70d82fe20d85583ae542eb8f76749dc640b0f13f682228819b8b2f04bd7a5a17a4c675540fe1c90

assert FLAG < P

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def inv(a):
    gcd, x, y = egcd(a % P, P)
    if gcd != 1:
        return -1
    else:
        return x % P

def add(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    i = inv(b[0] - a[0])
    if i == -1:
        return 0
    l = ((b[1] - a[1]) * i) % P
    x = (l*l - a[0] - b[0]) % P
    y = (l*(a[0] - x) - a[1]) % P
    return (x,y)

def double(a):
    if a == 0:
        return a
    i = inv(2*a[1])
    if i == -1:
        return 0
    l = ((3*a[0]*a[0] + A) * i) % P
    x = (l*l - 2*a[0]) % P
    y = (l*(a[0] - x) - a[1]) % P
    return (x,y)

def multiply(point, exponent):
    r0 = 0
    r1 = point
    for i in bin(exponent)[2:]:
        if i == '0':
            r1 = add(r0, r1)
            r0 = double(r0)
        else:
            r0 = add(r0, r1)
            r1 = double(r1)
    return r0

print(multiply((Gx,Gy),FLAG))

# Output:
# (10150325274093651859575658519947563789222194633356867789068177057343771571940302488270622886585658965620106459791565259790154958179860547267338437952379763L, 6795014289013853849339410895464797184780777251924203530417684718894057583288011725702609805686960505075072642102076744937056900144377846048950215257629102L)
