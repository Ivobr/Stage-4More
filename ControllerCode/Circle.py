
import math

r = 425
x = 420

xOpp = False
takeNeg = False

def getR(x, y):
    r = math.sqrt(x ** 2 + y ** 2)
    return r

def calcPoint(x,r, takeNeg):
    # (x-h)*(x-h) + (y + k)*(y + k) = r * r

    # (x*x)/r*r = -y*y

    # X^2/R^2 = y^2



    x *= x
    # print(x)
    r *= r
    # print(r)
    y2 = r-x
    # print(y2)

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


def call(x, r):
    global takeNeg, xOpp
    while True:
        if x > r:
            takeNeg = not takeNeg
            xOpp = not xOpp
            break
        calcPoint(x, r, takeNeg)

        if xOpp:
            x-= 1
        else:
            x +=1



# a = getA(500, 200)
# print("a: ", a)
# r = getR(500, 200)
# print("r: ",r)
# r += 50
#
# print(rincrement(r,a))
# x, y = rincrement(r, a)
# print(x)
# print(y)

call(x,r)