import random

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

def inverse_mod(a, m):
    if a < 0 or m <= a: a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod(d, c) + (c,)
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
    if ud > 0: return ud
    else: return ud + m

def checkpoint(x, y):
    if (x**3 + 7) % p == y**2 % p : return True
    else: return  False

def double(x, y):
    s = ((3 * x * x) * inverse_mod(2 * y, p)) % p
    x2 = (s*s - 2 * x) % p
    y2 = (s * (x - x2) - y) % p
    return x2, y2

def add(x1, y1, x2, y2):
    s = ((y2 - y1) * inverse_mod(x2 - x1, p)) % p 
    x3 = (s**2 - x2 - x1) % p
    y3 = (s * (x2- x3) - y2) % p 
    return x3, y3

def bit_to_add(a):
    d=[]
    bitl= a.bit_length()
    for i in range(bitl):
        c = a | (1 << i)
        if c == a: d.append(2**i)
    return d

def double_gen_point(x, y):
    points = {1:[x, y]}
    for i in range(1, r.bit_length()):
        x, y = double(x, y)
        points[2**i] = [x, y]
    return points

dbgen = double_gen_point(gx, gy)

def get_pubkey(n):
    if n >= r: return 'Out of range'
    if n in dbgen: return dbgen[n]
    btad = bit_to_add(n)
    point = dbgen[btad[0]]
    for i in btad[1:]:
        point = add(point[0], point[1], dbgen[i][0], dbgen[i][1])
    check = checkpoint(point[0], point[1])
    if check : return point
    else: return 0, 0


secret = random.randint(1, r-1)
pubkey = get_pubkey(secret)

print('Secret:', secret)
print('Pubkey:', pubkey)

