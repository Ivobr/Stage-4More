import time

import pygame

import calc
from fairino import Robot

robot = Robot.RPC('192.168.178.23')

x = 0
y = 0
z = 0
a = 0
r = 0
Moving = False

Xas = False
Yas = False
Zas = False
as4 = False
as5 = False
gripper = False

BigMove = False
BigMovement = 50
BigMovementA = 5

SmallMovement = 5
SmallMovementA = 0.5

takeNeg = False
xOpp = False

vel = 100
user = 0
tool = 0
blendT = 500  # experimenteer met waarde voor misschien een soepele beweging en stoppen wanneer nodig

rtn, pos = robot.GetActualTCPPose()
print(pos)
joystick = 0


def setup():
    global joystick

    # initaliseer controller
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


def moveCart(axis, direction):
    global x, y, r, a, takeNeg, xOpp, pos
    # rtn, pos = robot.GetActualTCPPose()
    # update de waarden van r en a voor als deze gewijzigt zijn
    r = calc.getR(pos[0], pos[1])
    a = calc.getA(pos[0], pos[1])

    match axis:
        case 0:
            if direction:
                if BigMove:
                    pos[0] += BigMovement
                    print("regel: 73 pos[0]:/x: ", pos[0])
                    if pos[0] > r:
                        takeNeg = not takeNeg
                        xOpp = not xOpp
                        pos[0] = r
                    print("regel: 78 pos[0]:/x: ", pos[0])
                    print("regel: 79 pos[1]:/y: ", pos[1])
                    pos[1], pos[0] = calc.calcPoint(pos[0], r, takeNeg)
                    print("regel: 81 pos[0]:/x: ", pos[0])
                    print("regel: 82 pos[1]:/y: ", pos[1])
                else:
                    pos[0] += SmallMovement
                    if pos[0] > r:
                        takeNeg = not takeNeg
                        xOpp = not xOpp
                        pos[0] = r
                    print("regel: 89 pos[0]:/x: ", pos[0])
                    print("regel: 90 pos[1]:/y: ", pos[1])
                    pos[1], pos[0] = calc.calcPoint(pos[0], r, takeNeg)
                    print("regel: 92 pos[0]:/x: ", pos[0])
                    print("regel: 93 pos[1]:/y: ", pos[1])
            else:
                if BigMove:
                    if pos[0] < -r:
                        takeNeg = not takeNeg
                        xOpp = not xOpp
                        pos[0] = r
                    pos[0] -= BigMovement
                    pos[1], pos[0] = calc.calcPoint(pos[0], r, takeNeg)
                else:
                    if pos[0] < -r:
                        takeNeg = not takeNeg
                        xOpp = not xOpp
                        pos[0] = r
                    pos[0] -= SmallMovement
                    pos[1], pos[0] = calc.calcPoint(pos[0], r, takeNeg)
            rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool, blendT=blendT)
        case 1:
            a = calc.getA(pos[0], pos[1])
            r = calc.getR(pos[0], pos[1])
            if direction:
                if BigMove:
                    r += BigMovement
                else:
                    r += SmallMovement
                x, y = calc.rIncrement(r, a)
                pos[0] = x
                pos[1] = y
                print(x, y)
            else:
                if BigMove:
                    r -= BigMovement
                else:
                    r -= SmallMovement
                x, y = calc.rIncrement(r, a)
                pos[0] = x
                pos[1] = y
            print(x, y)
            rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool, blendT=blendT)


# weghalen en in moveCart zetten
# misschien alleenbehouden voor as 4 en 5
def moveJ(axis, direction):
    print("Empty")
    rtn, pos = robot.GetActualJointPosDegree()
    match axis:
        # as 5
        case 5:
            if direction:
                if BigMove:
                    pos[4] += BigMovementA
                else:
                    pos[4] += SmallMovementA
            else:
                if BigMove:
                    pos[4] -= BigMovementA
                else:
                    pos[4] -= SmallMovementA
            robot.MoveJ(joint_pos=pos, vel=vel, user=user, tool=tool)

        case 6:
            if direction:
                if BigMove:
                    pos[5] += BigMovementA
                else:
                    pos[5] += SmallMovementA
            else:
                if BigMove:
                    pos[5] -= BigMovementA
                else:
                    pos[5] -= SmallMovementA
            if pos[5] > 174.9:
                pos[5] = 174
                print("Positive limit")
            elif pos[5] < -174.9:
                pos[5] = -174
                print("Negative limit")
            robot.MoveJ(joint_pos=pos, vel=vel, user=user, tool=tool)


def readJoystick():
    global joystick, BigMove, r, Xas, Yas, Zas, gripper
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()

    for i in range(axes):
        axis_val = joystick.get_axis(i)
        match i:
            # Linker joystick horizontaal
            case 0:
                if axis_val > 0.5:
                    print("Read left joystick")
                    if xOpp:
                        moveCart(i, 0)
                        Xas = True
                    elif not xOpp:
                        moveCart(i, 1)
                        Xas = True
                    else:
                        Xas = False
                elif axis_val < -0.5:
                    if xOpp:
                        moveCart(i, 1)
                        Xas = True
                    elif not xOpp:
                        moveCart(i, 0)
                        Xas = True
                    else:
                        Xas = False
                else:
                    Xas = False

            # Linker joystick Verticaal
            case 1:
                if axis_val > 0.5:
                    moveCart(i, 1)
                    Yas = True
                elif axis_val < -0.5:
                    moveCart(i, 0)
                    Yas = True
                else:
                    Yas = False

            # Rechter joystick as 5
            # moet nog switch in komen voor de grijper
            case 2:
                if axis_val > 0.5:
                    if gripper:
                        moveJ(6, 1)
                    else:
                        moveJ(5, 1)
                elif axis_val < -0.5:
                    if gripper:
                        moveJ(6, 0)
                    else:
                        moveJ(5, 0)

            # Rechter joystick as 4
            case 3:
                if axis_val > 0.5:
                    moveJ(i, 1)
                elif axis_val < -0.5:
                    moveJ(i, 0)
            # L2 = z-as omlaag

    for i in range(buttons):
        button_val = joystick.get_button(i)
        if button_val:
            match i:

                case 9:
                    BigMove = False
                    print("BIG MOVE FALSE")
                case 10:
                    BigMove = True
                    print("BIG MOVE TRUE")
                case 15:
                    gripper = not gripper
                    robot.SetDO(0, gripper)


def main():
    global r, Xas, Yas, Zas, pos
    rtn, pos = robot.GetActualTCPPose()
    r = calc.getR(pos[0], pos[1])
    while True:
        readJoystick()
        if Xas == False and Yas == False and Zas == False:
            robot.MotionQueueClear()
            rtn, pos = robot.GetActualTCPPose()
            print(pos)


if __name__ == "__main__":
    try:
        setup()
        main()
    except KeyboardInterrupt:
        robot.ResetAllError()
        robot.CloseRPC()
    finally:
        robot.ResetAllError()
        robot.CloseRPC()
