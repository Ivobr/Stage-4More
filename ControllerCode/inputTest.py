import pygame

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

Xas = Yas = Zas = S5 = False
lastValY = lastValZ = lastValX = lastValS5 = 0


def calc(axis_val):
    vel = (axis_val * 100)/2
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
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        # JOG(1, 1, axis_val, 2)
                        print("Update")
                        lastValX = axis_val
                    Xas = True
                    print(axis_val)
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        # JOG(1,0,axis_val, 2)
                        lastValX = axis_val
                    Xas = True
                    print(axis_val)
                else:
                    Xas = False
            case 1:
                if axis_val > 0.1:
                    if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
                        # JOG(2, 1, axis_val, 2)
                        print("Update")
                        lastValY = axis_val
                    Yas = True
                    print(axis_val)
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
                        # JOG(2, 0, axis_val, 2)
                        lastValY = axis_val
                    Yas = True
                    print(axis_val)
                else:
                    Yas = False
            case 2:

                if axis_val > 0.1:
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:

                        print(axis_val)
                        lastValS5 = axis_val
                    S5 = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:

                        print(axis_val)
                        lastValS5 = axis_val
                    S5 = True
                else:
                    S5 = False
            case 4:
                if axis_val > -0.9:
                    axis_val = axis_val + 1
                    # rtn = robot.StartJOG(2,3,0, 10000)
                    print(axis_val)
                    calc(axis_val)
                    Zas = True
                else:
                    Zas = False
            case 5:
                if axis_val > -0.9:
                    # rtn = robot.StartJOG(2,3,1,10000)
                    Zas = True
                    print(axis_val)
                else:
                    Zas = False
        if Xas == False and Yas == False and Zas == False and S5 == False:
            # robot.StopJOG(3)
            lastValZ = lastValY = lastValX = lastValS5 = 0
            print("little big ")