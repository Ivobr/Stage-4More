
from fairino import Robot
import time
import pygame


Xas = Yas = Zas = S5 = S4 = False

ref = 2
lastValX = lastValY = lastValZ = lastValS5 = lastValS4 = 0

robot = Robot.RPC('192.168.178.23')

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


def JOG(nb, dir, vel, ref):
    robot.StopJOG(3)
    time.sleep(0.1)
    vel = (vel*100)/2


    print("Stoped")
    rtn = robot.StartJOG(ref=ref, nb=nb, dir=dir, max_dis=10000, vel=vel)
    print("Continued")
    print(rtn)
    print(vel)

def height(nb, dir, axis_val):
    robot.StopJOG(3)
    time.sleep(0.1)

    print("Two number nine's")
    vel = (axis_val*100)/4 # / = 2 * groter dan bij normale
    print(vel)
    rtn = robot.StartJOG(ref=2, nb=nb, dir=dir, max_dis=10000, vel=vel)
    print(rtn)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    axes = joystick.get_numaxes()
    for i in range(axes):
        axis_val = joystick.get_axis(i)
        match i:
            case 0:
                if axis_val > 0.1:
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        JOG(1, 1, axis_val, 2)
                        print("Update")
                        lastValX = axis_val
                    Xas = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        JOG(1,0,axis_val, 2)
                        lastValX = axis_val
                    Xas = True
                else:
                    Xas = False
            case 1:
                if axis_val > 0.1:
                    if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
                        JOG(2, 1, axis_val, 2)
                        print("Update")
                        lastValY = axis_val
                    Yas = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
                        JOG(2, 0, axis_val, 2)
                        lastValY = axis_val
                    Yas = True
                else:
                    Yas = False
            # rechter joystick
            case 2:
                if axis_val > 0.1:
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                        JOG(5,1, axis_val, 0)
                        print(axis_val)
                        lastValS5 = axis_val
                    S5 = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                        JOG(5, 0, axis_val, 0)
                        print(axis_val)
                        lastValS5 = axis_val
                    S5 = True
                else:
                    S5 = False

            case 3:
                if axis_val > 0.1:
                    if axis_val - lastValS4 > 0.1 or axis_val - lastValS4 < -0.1:
                        print("pos")
                        JOG(4, 1, axis_val, 0)
                        print(axis_val)
                        lastValS4 = axis_val
                    S4 = True
                elif axis_val < -0.1:
                    print("neg")
                    axis_val = abs(axis_val)
                    if axis_val - lastValS4 > 0.1 or axis_val - lastValS4 < -0.1:
                        JOG(4, 0, axis_val, 0)
                        print(axis_val)
                        lastValS4 = axis_val
                    S4 = True
                else:
                    S4 = False
            # L2
            case 4:
                if axis_val > -0.9:
                    print(axis_val)
                    axis_val += 1
                    if axis_val - lastValZ > 0.2 or axis_val - lastValZ < -0.2:
                        height(3, 0, axis_val)
                        lastValZ = axis_val
                    Zas = True
                else:
                    Zas = False
            # R2
            case 5:
                if axis_val > -0.9:
                    axis_val += 1
                    if axis_val - lastValZ > 0.2 or axis_val - lastValZ < -0.2:
                        height(3, 1, axis_val)
                        lastValZ = axis_val
                    Zas = True

                else:
                    Zas = False
        if Xas == False and Yas == False and Zas == False and S5 == False and S4 == False:
            robot.StopJOG(3)
            lastValX = lastValY = lastValZ = lastValS4 = lastValS5 = 0
        # else:
            # print("Xas = ", Xas)
            # print("Yas = ", Yas)
            # print("Kop = ", kop)
            # print("Kop2 = ", kop2)
