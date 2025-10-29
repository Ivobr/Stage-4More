import cmath

r = 425
def calcPoint(x,r):
    # (x-h)*(x-h) + (y + k)*(y + k) = r * r

    # (x*x)/r*r = -y*y

    # X^2/R^2 = y^2

    x *= x
    print(x)
    r *= r
    print(r)
    y2 = r-x
    print(y2)

    y = cmath.sqrt(y2)
    return y



print("y = ",calcPoint(300, r))