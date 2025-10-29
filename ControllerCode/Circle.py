
import math

r = 425
takeNeg = False

def getR(x, y):
    global r
    x *= x
    y *= y
    r2 = x + y
    r = math.sqrt(r2)
    return r

def calcPoint(x,r):
    global takeNeg
    # (x-h)*(x-h) + (y + k)*(y + k) = r * r

    # (x*x)/r*r = -y*y

    # X^2/R^2 = y^2

    if x > r:
        takeNeg = True
        return takeNeg

    x *= x
    print(x)
    r *= r
    print(r)
    y2 = r-x
    print(y2)

    y = math.sqrt(y2)
    if takeNeg:
        y = -y

    print(y)
    return y

def rincrement(r, a):
    # r = nieuwe radius
    # hoek J1

    a = math.radians(a)
    x = r * math.cos(a)
    y = r * math.sin(a)

    return x,y


def getA(x, y):
    angle = y/x
    a = math.atan(angle)
    angles = math.degrees(a)
    return angles




a = getA(500, 200)
print("a: ", a)
r = getR(500, 200)
print("r: ",r)
r += 50

print(rincrement(r,a))
x, y = rincrement(r, a)
print(x)
print(y)