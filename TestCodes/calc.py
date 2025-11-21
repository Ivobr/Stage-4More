import math


def getA(x, y):
    angle = math.atan2(y, x)  # Overstaand / Aanliggend
    a = math.degrees(angle)  # reken van radiale naar graden
    return a


# Straal verkrijgen
def getR(x, y):
    # pytaghoras a + b = c
    r = math.sqrt((x ** 2) + (y ** 2))
    return r


# Straal verhogen
# return x en y
def increaseR(r, a):
    # r = nieuwe straal
    # a = huidige hoek van kop tot x as
    a = math.radians(a)
    x = r * math.cos(a)
    y = r * math.sin(a)
    return x, y
