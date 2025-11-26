# *
# Code met alles bij elkaar
#   Controller aansturen
#       JOG (Voor J1, J4 t/m 6 en Z-as)
#       MoveCart of ServoCart voor vergroting rotatieas
#       Noodknop controller
#       Grijper 1 mm vergroting voor minder druk
#   Safety functies
#       Pos en neg limit voor graden
#       Checken of de limits voor alles nog goed ingesteld staat
#
#
#
#   Door blendT aan te passen naar -1.0 kunnen er stappen genomen worden i.p.v. smooth bewegingen*#

import time

import pygame

import calc
from fairino import Robot

# *
# Eigenlijk is het gewoon controller 3 met een MoveCart i.p.v. ServoCart*#
robot = Robot.RPC('192.168.178.23')

joystick = 0

# Voor rotatie increase
r = 0
a = 0
count = 0

# Safety settings
secure = [4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
mode = 0
config = 1

# Robot settings
user = 0
tool = 0
blendT = 1
vel = 100
pos = []

lastValRo = lastValRoInc = lastValZup = lastValZdown = lastValS5 = lastValS4 = 0

# bewegingen booleans
Rotation = False
RotationInc = False
ZasUp = False
ZasDown = False
S5 = False
S4 = False
gripper = False
stopped = False


def setup():
    global joystick, r, a, pos, mode, secure, config
    rtn, pos = robot.GetActualTCPPose()

    # initializer controller
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # zet safety instellingen zodat bij contact de arm stopt
    rtn = robot.SetAnticollision(mode, secure, config)
    print("Anticollision set: ", rtn)
    rtn = robot.SetCollisionStrategy(3, 2000, 100, 250)
    print("CollisionStrategy set: ", rtn)

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
    global lastValRoInc, vel, stopped, count
    stopped = False
    rtn, size = robot.GetMotionQueueLength()
    if count > 3:
        if size < 2:
            count = 0
        return
    if axis_val - lastValRoInc > 0.1 or axis_val - lastValRoInc < -0.1:
        vel = (axis_val * 100) / 2
        lastValRoInc = axis_val
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
    else:
        vel = (axis_val * 100) / 2
        if gripper:
            rtn = robot.StartJOG(ref=0, nb=6, dir=direction,
                                 max_dis=10000, vel=vel)
        else:
            rtn = robot.StartJOG(
                ref=0, nb=number, dir=direction, max_dis=10000, vel=vel)


def readJoystick():
    global joystick, Rotation, RotationInc, ZasDown, ZasUp, S5, S4, lastValRo, lastValRoInc, lastValZdown, lastValZup, lastValS4, lastValS5, gripper
    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i in range(axes):
        axis_val = joystick.get_axis(i)
        match i:
            # Rotation via JOG J1
            case 0:
                if axis_val > 0.1:
                    if axis_val - lastValRo > 0.1 or axis_val - lastValRo < -0.1:
                        # Nog eff checken of die niet de andere kant op moet
                        JOG(1, 1, axis_val)
                        lastValRo = axis_val
                    Rotation = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValRo > 0.1 or axis_val - lastValRo < -0.1:
                        # Nog eff checken of die niet de andere kant op moet
                        JOG(1, 0, axis_val)
                        lastValRo = axis_val
                    Rotation = True
                else:
                    Rotation = False
            case 1:
                if axis_val > 0.1:
                    IncreaseR(axis_val, 0)
                    RotationInc = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    IncreaseR(axis_val, 1)
                    RotationInc = True
                else:
                    RotationInc = False
            case 2:
                # as 5 and gripper
                if axis_val > 0.1:
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                        JOG(5, 0, axis_val)
                        lastValS5 = axis_val
                    S5 = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                        JOG(5, 1, axis_val)
                        lastValS5 = axis_val
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
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValS4 > 0.1 or axis_val - lastValS4 < -0.1:
                        JOG(4, 1, axis_val)
                        lastValS4 = axis_val
                    S4 = True
                else:
                    S4 = False

            case 4:
                # L and R2 start at -1.0 so make them  > 0
                axis_val += 1
                if axis_val > 0.1:
                    if axis_val - lastValZdown > 0.2 or axis_val - lastValZdown < -0.2:
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
    global r, a, Rotation, RotationInc, ZasDown, ZasUp, S4, S5, stopped
    print("Main")

    setup()
    while True:
        readJoystick()
        if Rotation == False and RotationInc == False and ZasDown == False and ZasUp == False and S4 == False and S5 == False and stopped == False:
            robot.StopJOG(3)
            robot.StopMotion()
            robot.MotionQueueClear()
            stopped = True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        robot.CloseRPC()
        print("Stopped")
