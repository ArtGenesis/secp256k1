import random

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
gz = 0x1

def inverse_mod(a, m):
    if a < 0 or m <= a: a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod(d, c) + (c,)
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
    if ud > 0: return ud
    else: return ud + m

def from_jacobian(Xp, Yp, Zp):
    z = inverse_mod(Zp, p)
    return (Xp * z**2) % p, (Yp * z**3) % p

def checkpoint(x, y):
    if (x**3 + 7) % p == y**2 % p : return True
    else: return  False

def bit_to_add(a):
    d=[]
    bitl= a.bit_length()
    for i in range(bitl):
        c = a | (1 << i)
        if c == a: d.append(2**i)
    return d

def double_gen_point(x, y, z):
    points = {1:[x, y, z]}
    for i in range(1, r.bit_length()):
        x, y, z = double(x, y, z)
        points[2**i] = [x, y, z]
    return points

def double(x, y, z):
    s = 4 * x * y**2 % p
    m = 3 * x**2 % p
    x1 = (m**2 - 2 * s) % p
    y1 = (m * (s - x1) - 8 * y**4) % p
    z1 = 2 * y * z % p
    return x1, y1, z1

def add(Xp, Yp, Zp, Xq, Yq, Zq):
    if not Yp: return (Xq, Yq, Zq)
    if not Yq: return(Xp, Yp, Zp)
    u1 = (Xp * Zq**2) % p
    u2 = (Xq * Zp**2) % p
    s1 = (Yp * Zq**3) % p
    s2 = (Yq * Zp**3) % p
    if u1 == u2:
        if s1 != s2: return(0,0,1)
        return jacobian_double(Xp, Yp, Zp)
    h = u2 - u1
    rs = s2 - s1
    h2 = (h * h) % p
    h3 = (h * h2) % p
    u1h2 = (u1 * h2) % p
    nx = (rs**2 - h3 - 2*u1h2) % p
    ny = (rs*(u1h2 - nx) - s1 * h3) % p
    nz = (h*Zp*Zq) % p
    return nx, ny, nz

dbgen = double_gen_point(gx, gy, gz)

def get_pubkey(n):
    if n >= r: return 'Out of range'
    if n in dbgen: return from_jacobian(dbgen[n][0], dbgen[n][1], dbgen[n][2])
    btad = bit_to_add(n)
    point = dbgen[btad[0]]
    for i in btad[1:]:
        point = add(point[0], point[1], point[2], dbgen[i][0], dbgen[i][1], dbgen[i][2])
    point = from_jacobian(point[0], point[1], point[2])
    check = checkpoint(point[0], point[1])
    if check : return point
    else: return 0, 0

secret = random.randint(1, r-1)
pubkey = get_pubkey(secret)

print('Secret:', secret)
print('Pubkey:', pubkey)

