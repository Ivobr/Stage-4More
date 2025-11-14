import math


def getA(x, y):
    # bereken de hoek van de arm ten opzichten van het middelpunt
    # doormiddel van de tan van x en y te nemen

    angle = math.atan(y / x)  # Overstaand / Aanligend
    a = math.degrees(angle)  # reken van radiale naar graden
    return a


def getR(x, y):
    # bereken de afstand van het middelpunt tot de kop van de arm
    # Doormiddel van de cirkel formule x^2 + y^2 = r^2
    r = math.sqrt(x ** 2 + y ** 2)
    return r


def rIncrement(r, a):
    # vergroot de afstand tussen het middelpunt en de kop van de arm
    # Doormiddel van het uitkrekenen van de nieuwe overstaande (y) en aanliggende zijde (x)
    a = math.radians(a)
    x = r * math.cos(a)
    y = r * math.sin(a)

    print("rIncrement = ", x, " ", y)
    return x, y


def calcPoint(x, r, takeNeg):
    # draai de kop van de arm rond het middelpunt met dezelfde as
    # Doormiddel van het uitrekenen van de y waarde binnen de cirkel formule x^2 + y^2 = r^2

    # * formule:
    # x^2 + y^2 = r^2
    # y^2 = r^2 + x^2
    # *#
    if x > r:
        x = r
    elif x < -r:
        x = -r
    y = math.sqrt(r ** 2 - x ** 2)
    # print("CalcPoint Y = ", y)

    # voor als de negative waarde van y genomen moet worden om "onder" de x-as te komen
    if takeNeg:
        y = -y
        return y, x
    else:
        return y, x


y, x = calcPoint(-626, 425, 0)
print(x)
