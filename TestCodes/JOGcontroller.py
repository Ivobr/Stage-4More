from fairino import Robot
import time
import pygame


Xas = False
Yas = False
ref = 2
lastVal = 0

robot = Robot.RPC('192.168.178.23')

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

def stop():
    robot.StopJOG(3)
def JOG(nb, dir, vel):
    if dir == 0:
        vel = (vel * -100)/2
    else:
        vel = (vel*100)/2


    print("Stoped")
    rtn = robot.StartJOG(ref=ref, nb=nb, dir=dir, max_dis=10000, vel=vel)
    print("Continued")
    print(rtn)
    print(vel)


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
                    if axis_val - lastVal > 0.2 or axis_val - lastVal < -0.2:
                        stop()
                        time.sleep(0.1)
                        JOG(1, 1, axis_val)
                        print("Update")
                        lastVal = axis_val
                    Xas = True
                elif axis_val < -0.5:
                    robot.StartJOG(ref=ref, nb=1, dir=0, max_dis=10000)
                    Xas = True
                else:
                    Xas = False
            case 1:
                if axis_val > 0.5:
                    robot.StartJOG(ref=ref, nb=2, dir=0, max_dis=10000)
                    Yas = True
                elif axis_val < -0.5:
                    robot.StartJOG(ref=ref, nb=2, dir=1, max_dis=10000)
                    Yas = True
                else:
                    Yas = False
        if Xas == False and Yas == False:
            robot.StopJOG(3)
            lastVal = 0
            # print("Yas = ", Yas)
        # else:
            # print("Xas = ", Xas)
            # print("Yas = ", Yas)
