
import math

r = 425
takeNeg = False
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
    print()



print("y = ",calcPoint(425, r))