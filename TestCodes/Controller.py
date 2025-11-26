import time

import pygame

import calc
from fairino import Robot

# *
# Eigenlijk is het gewoon controller 3 met een MoveCart i.p.v. ServoCart*#
robot = Robot.RPC('192.168.178.23')

joystick = 0

user = 0
tool = 0
blendT = 1
vel = 100
pos = []

x = 0
y = 0
z = 0
r = 0
a = 0
count = 0

lastValX = lastValY = lastValZup = lastValZdown = lastValS5 = lastValS4 = 0

# bewegingen booleans
Xas = False
Yas = False
ZasUp = False
ZasDown = False
S5 = False
S4 = False
gripper = False
stopped = False


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


def stop():
    robot.StopMotion()
    robot.DragTeachSwitch(1)
    time.sleep(5)
    robot.DragTeachSwitch(0)


def IncreaseR(axis_val, direction):
    global lastValY, vel, stopped, count
    stopped = False
    rtn, size = robot.GetMotionQueueLength()
    print(count)
    if count > 3:
        if size < 2:
            count = 0
        return
    if axis_val - lastValY > 0.1 or axis_val - lastValY < -0.1:
        vel = (axis_val * 100) / 2
        lastValY = axis_val
    rtn, pos = robot.GetActualTCPPose()
    r = calc.getR(pos[0], pos[1])
    a = calc.getA(pos[0], pos[1])

    if direction:
        r += 100
    else:
        r -= 100

    pos[0], pos[1] = calc.increaseR(r, a)
    rtn = robot.MoveCart(desc_pos=pos, tool=tool,
                         user=user, vel=vel, blendT=blendT)
    count += 1


# Herschrijven voor test de += 1 in de switch case zetten in de main
def JOG(number, direction, axis_val):
    global gripper, stopped
    stopped = False
    robot.StopJOG(3)
    # little sleep to reset
    time.sleep(0.1)
    if number == 2:
        vel = (axis_val * 100) / 4
        rtn = robot.StartJOG(ref=2, nb=3, dir=direction,
                             max_dis=10000, vel=vel)
    elif number == 5:
        vel = (axis_val * 100) / 2
        if gripper:
            rtn = robot.StartJOG(ref=0, nb=6, dir=direction,
                                 max_dis=10000, vel=vel)
        else:
            rtn = robot.StartJOG(
                ref=0, nb=number, dir=direction, max_dis=10000, vel=vel)

    else:
        vel = (axis_val * 100) / 2
        rtn = robot.StartJOG(
            ref=0, nb=number, dir=direction, max_dis=10000, vel=vel)
    print(rtn)


def readJoystick():
    global joystick, Xas, Yas, ZasDown, ZasUp, S5, S4, lastValX, lastValY, lastValZdown, lastValZup, lastValS4, lastValS5, gripper
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
                        print(
                            "if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:")
                        print(axis_val)
                        # Nog eff checken of die niet de andere kant op moet
                        JOG(1, 1, axis_val)
                        lastValX = axis_val
                    Xas = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        # Nog eff checken of die niet de andere kant op moet
                        JOG(1, 0, axis_val)
                        lastValX = axis_val
                    Xas = True
                else:
                    Xas = False
            case 1:
                if axis_val > 0.1:
                    IncreaseR(axis_val, 0)
                    Yas = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    IncreaseR(axis_val, 1)
                    Yas = True
                else:
                    Yas = False
            case 2:
                # as 5 and gripper
                if axis_val > 0.1:
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                        JOG(5, 0, axis_val)
                        lastValS5 = axis_val
                    S5 = True
                    print(axis_val)
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                        JOG(5, 1, axis_val)
                        lastValS5 = axis_val

                    print(";")
                    S5 = True
                else:
                    S5 = False
            case 3:
                # as 4
                if axis_val > 0.1:
                    if axis_val - lastValS4 > 0.1 or axis_val - lastValS4 < -0.1:
                        JOG(4, 0, axis_val)
                        lastValS4 = axis_val
                    S4 = True
                    print(axis_val)
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValS4 > 0.1 or axis_val - lastValS4 < -0.1:
                        JOG(4, 1, axis_val)
                        lastValS4 = axis_val

                    print(";")
                    S4 = True
                else:
                    S4 = False

            case 4:
                # L and R2 start at -1.0 so make them  > 0
                axis_val += 1
                if axis_val > 0.1:
                    if axis_val - lastValZdown > 0.2 or axis_val - lastValZdown < -0.2:
                        print(
                            " if axis_val - lastValZdown > 0.2 or axis_val - lastValZdown < -0.2:")
                        JOG(2, 0, axis_val)
                        lastValZdown = axis_val
                    ZasDown = True
                else:
                    ZasDown = False
            case 5:
                axis_val += 1
                if axis_val > 0.1:
                    if axis_val - lastValZup > 0.2 or axis_val - lastValZup < -0.2:
                        JOG(2, 1, axis_val)
                        lastValZup = axis_val
                    ZasUp = True
                else:
                    ZasUp = False

    for i in range(buttons):
        button_val = joystick.get_button(i)
        if button_val:
            match i:
                case 0:
                    robot.MoveGripper(2, 100, 100, 1, 5000, 1, 0, 0, 0, 0)
                    time.sleep(2)
                    rtn, err, pos = robot.GetGripperCurPosition()
                    print(pos)
                    pos -= 1
                    robot.MoveGripper(2, pos, 100, 1, 5000, 1, 0, 0, 0, 0)
                case 1:
                    robot.MoveGripper(2, 0, 100, 100, 10000, 0, 0, 0, 0, 0)
                case 5:
                    print("Noodknop functie")
                    stop()
                case 15:
                    gripper = not gripper
                    robot.SetDO(0, gripper)
                    time.sleep(1)


def main():
    global r, a, Xas, Yas, ZasDown, ZasUp, S4, S5, stopped
    print("Main")

    setup()
    while True:
        readJoystick()
        if Xas == False and Yas == False and ZasDown == False and ZasUp == False and S4 == False and S5 == False and stopped == False:
            robot.StopJOG(3)
            robot.StopMotion()
            print(robot.GetMotionQueueLength())
            robot.MotionQueueClear()
            print(robot.GetMotionQueueLength())
            stopped = True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        robot.CloseRPC()
        print("Stopped")
