import pygame
import time

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

Xas = Yas = ZasUp = ZasDown = S5 = S4 = False
lastValX = lastValY = lastValZup = lastValZdown = lastValS5 = lastValS4 = 0

values = [0,0,0,0,0,0]
TrueValues = [0,0,0,0,0,0]


def calc(axis_val):
    vel = (axis_val * 100)/2
    print(vel)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    axes = joystick.get_numaxes()
    # time.sleep(1)
    for i in range(axes):
        axis_val = joystick.get_axis(i)

        if i >= 4:
            axis_val += 1

        if axis_val < 0:
            TrueValues[i] = axis_val
            axis_val = abs(axis_val)
        else:
            TrueValues[i] = axis_val


        values[i] = axis_val

        # print(values)



    element = max(values)
    i = values.index(element)
    axis_val = TrueValues[i]
    match i:
        case 0:
            if axis_val > 0.1:
                if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                    print("Linker=,", axis_val)
                    lastValX = axis_val
                Xas = True
            elif axis_val < -0.1:
                axis_val = abs(axis_val)
                if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                    print("Linker links=,", axis_val)
                    lastValX = axis_val
                Xas = True
            else:
                Xas = False
        case 1:
            if axis_val > 0.1:
                if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
                    print("Linker omlaag=,", axis_val)
                    lastValY = axis_val
                Yas = True
            elif axis_val < -0.1:
                axis_val = abs(axis_val)
                if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
                    lastValY = axis_val
                    print("Linker omhoog =,", axis_val)
                Yas = True
            else:
                Yas = False
        # rechter joystick
        case 2:
            if axis_val > 0.1:
                if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                    print("Rechter hori=,", axis_val)
                    lastValS5 = axis_val
                S5 = True
            elif axis_val < -0.1:
                axis_val = abs(axis_val)
                if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                    print("Rechter hori=,", axis_val)
                    lastValS5 = axis_val
                S5 = True
            else:
                S5 = False

        case 3:
            if axis_val > 0.1:
                if axis_val - lastValS4 > 0.1 or axis_val - lastValS4 < -0.1:
                    print("Rechter hoog=,", axis_val)
                    lastValS4 = axis_val
                S4 = True
            elif axis_val < -0.1:
                print("neg")
                axis_val = abs(axis_val)
                if axis_val - lastValS4 > 0.1 or axis_val - lastValS4 < -0.1:
                    print(axis_val)
                    lastValS4 = axis_val
                S4 = True
            else:
                S4 = False
        # L2
        case 4:
            if axis_val > 0.1:
                if axis_val - lastValZdown > 0.2 or axis_val - lastValZdown < -0.2:
                    lastValZdown = axis_val
                    print("L2")
                ZasDown = True
            else:
                ZasDown = False
        # R2
        case 5:
            if axis_val > 0.1:
                if axis_val - lastValZup > 0.2 or axis_val - lastValZup < -0.2:
                    lastValZup = axis_val
                    print("R2")
                ZasUp = True

            else:
                ZasUp = False
    if  Xas == False and Yas == False and ZasUp == False and ZasDown == False and S5 == False and S4 == False:
        # robot.StopJOG(3)
        lastValZ = lastValY = lastValX = lastValS5 = 0
        print("little big ")