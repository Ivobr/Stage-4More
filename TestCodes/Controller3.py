import time

import pygame

import calc
from fairino import Robot

robot = Robot.RPC('192.168.178.23')

joystick = 0

user = 0
tool = 0
blendT = 500
vel = 100
pos = []

x = 0
y = 0
z = 0
r = 0
a = 0

lastValX = lastValY = lastValZup = lastValZdown = lastValS5 = lastValS4 = 0

# bewegingen booleans
Xas = False
Yas = False
ZasUp = False
ZasDown = False
S5 = False
S4 = False


def setup():
    global joystick, r, a, pos
    rtn, pos = robot.GetActualTCPPose()

    # initializer controller
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # reset en activeer de grijper
    robot.ActGripper(2, 0)
    time.sleep(1)
    rtn = robot.ActGripper(2, 1)
    time.sleep(3)
    print(rtn)

    r = calc.getR(pos[0], pos[1])
    a = calc.getA(pos[0], pos[1])
    print(r, a)


def IncreaseR(axis_val, direction):
    # Function only for axis 1
    vel = (axis_val * 100) / 2
    print(vel)

    rtn, pos = robot.GetActualTCPPose()
    r = calc.getR(pos[0], pos[1])
    a = calc.getA(pos[0], pos[1])
    if direction:
        r += 10
    else:
        r -= 10
    pos[0], pos[1] = calc.increaseR(r, a)
    rtn = robot.MoveCart(desc_pos=pos, tool=tool, user=user, vel=vel, blendT=blendT)
    print(rtn)

    print("Not scary for me")


def JOG(number, direction, axis_val):
    robot.StopJOG(3)
    # little sleep to reset
    time.sleep(0.1)
    if number == 4 or number == 5:
        vel = (axis_val * 100) / 4
        print("Speed for ax 4 and 5 ", vel)
        rtn = robot.StartJOG(ref=2, nb=3, dir=direction, max_dis=10000, vel=vel)
    else:
        vel = (axis_val * 100) / 2
        rtn = robot.StartJOG(ref=0, nb=number, dir=direction, max_dis=10000, vel=vel)
    print(rtn)


def readJoystick():
    global joystick, Xas, Yas, ZasDown, ZasUp, lastValX, lastValY, lastValZdown, lastValZup
    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i in range(axes):
        axis_val = joystick.get_axis(i)
        match i:
            # Xas via JOG J1
            case 0:
                if axis_val > 0.1:
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        print("if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:")
                        print(axis_val)
                        JOG(1, 1, axis_val)  # Nog eff checken of die niet de andere kant op moet
                        lastValX = axis_val
                    Xas = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        JOG(1, 0, axis_val)  # Nog eff checken of die niet de andere kant op moet
                        lastValX = axis_val
                    Xas = True
                else:
                    Xas = False
            case 1:
                if axis_val > 0.1:
                    if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
                        # Needs to be decreasing
                        IncreaseR(axis_val, 0)  # Axis_val, direction
                        lastValY = axis_val
                    Yas = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
                        # Needs to be increasing
                        IncreaseR(axis_val, 1)
                        lastValY = axis_val
                    Yas = True
                else:
                    Yas = False
            case 4:
                # L and R2 start at -1.0 so make them  > 0
                axis_val += 1
                if axis_val > 0.1:
                    if axis_val - lastValZdown > 0.2 or axis_val - lastValZdown < -0.2:
                        print(" if axis_val - lastValZdown > 0.2 or axis_val - lastValZdown < -0.2:")
                        JOG(4, 0, axis_val)
                        lastValZdown = axis_val
                    ZasDown = True
                else:
                    ZasDown = False
            case 5:
                axis_val += 1
                if axis_val > 0.1:
                    if axis_val - lastValZup > 0.2 or axis_val - lastValZup < -0.2:
                        print(" if axis_val - lastValZdown > 0.2 or axis_val - lastValZdown < -0.2:")
                        JOG(5, 1, axis_val)
                        lastValZup = axis_val
                    ZasUp = True
                else:
                    ZasUp = False


def main():
    global r, a, Xas, Yas, ZasDown, ZasUp
    print("Main")

    setup()
    while True:
        readJoystick()
        if Xas == False and Yas == False and ZasDown == False and ZasUp == False:
            robot.StopJOG(3)
            robot.StopMotion()
            print(robot.GetMotionQueueLength())
            robot.MotionQueueClear()
            print(robot.GetMotionQueueLength())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        robot.CloseRPC()
        print("Stopped")
