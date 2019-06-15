p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8


pcb = 0x7ae96a2b657c07106e64479eac3434e99cf0497512f58995c1396c28719501ee
pcb2 = 0x851695d49a83f8ef919bb86153cbcb16630fb68aed0a766a3ec693d68e6afa40
p9 = 0x1c71c71c71c71c71c71c71c71c71c71c71c71c71c71c71c71c71c71c555554e9
p4 = 0x3fffffffffffffffffffffffffffffffffffffffffffffffffffffffbfffff0c

def checkpoint(x, y):
    if (x**3 + 7) % p == y**2 % p : return True
    else: return  False

# return two Y coordinates from X such (x**3+7) % p == y**2 % p
def return_y_from_x(x):
    y2 = (x**3 + 7) % p
    yu = pow(y2, p4, p)
    yd = p - yu
    if checkpoint(x, yu): return yu, yd
    else: return 'Point with such x coordinates does not exist'

# return three X coordinates from Y such (x**3+7) % p == y**2 % p
def return_x_from_y(y):
    xu = (y**2 % p) - 7
    x1 = pow(xu, p9, p)
    if x1**3 % p == xu % p:
        x2 = x1 * pcb % p
        x3 = x1 * pcb2 % p
        return x1, x2, x3
    else: return 'Point with such y coordinates does not exist'


X = return_x_from_y(gy)
print('X-Coordinates:', X)

Y = return_y_from_x(gx)
print('Y-Coordinates:', Y)
