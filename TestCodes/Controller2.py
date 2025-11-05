from fairino import Robot
import time
import pygame
import calc

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

    # update de waarden van r en a voor als deze gewijzigt zijn
    r = calc.getR(pos[0], pos[1])
    a = calc.getA(pos[0], pos[1])

    match axis:
        case 0:
            if direction:
                if BigMove:
                    pos[0] += BigMovement
                    if pos[0] > r:
                        takeNeg = not takeNeg
                        xOpp = not xOpp
                        pos[0] = r
                    pos[1] = calc.calcPoint(pos[0], r, takeNeg)
                else:
                    pos[0] += SmallMovement
                    if pos[0] > r:
                        takeNeg = not takeNeg
                        xOpp = not xOpp
                        pos[0] = r
                    pos[1] = calc.calcPoint(pos[0], r, takeNeg)
            else:
                if BigMove:
                    if pos[0] < -r:
                        takeNeg = not takeNeg
                        xOpp = not xOpp
                        pos[0] = r
                    pos[0] -= BigMovement
                    pos[1] = calc.calcPoint(pos[0], r, takeNeg)
                else:
                    if pos[0] < -r:
                        takeNeg = not takeNeg
                        xOpp = not xOpp
                        pos[0] = r
                    pos[0] -= SmallMovement
                    pos[1] = calc.calcPoint(pos[0], r, takeNeg)
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
def moveJ(axis, direction):
    print("Empty")
    rtn, pos = robot.GetActualJointPosDegree()
    match axis:
        case 2:
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

        case 3:
            if direction:
                if BigMove:
                    pos[3] += BigMovementA
                else:
                    pos[3] += SmallMovementA
            else:
                if BigMove:
                    pos[3] -= BigMovementA
                else:
                    pos[3] -= SmallMovementA
            robot.MoveJ(joint_pos=pos, vel=vel, user=user, tool=tool)

        # gaat weg wordt vervangen met de switch van de boolean voor as 6
        case 13:
            if BigMove:
                pos[5] += BigMovementA
            else:
                pos[5] += SmallMovementA
            robot.MoveJ(joint_pos=pos, vel=vel, user=user, tool=tool)
            print("13")

        case 14:
            if BigMove:
                pos[5] -= BigMovementA
            else:
                pos[5] -= SmallMovementA
            robot.MoveJ(joint_pos=pos, vel=vel, user=user, tool=tool)
            print("14")


def readJoystick():
    global joystick, BigMove, r, Xas, Yas, Zas
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()

    for i in range(axes):
        axis_val = joystick.get_axis(i)
        match i:
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
            case 1:
                if axis_val > 0.5:
                    moveCart(i, 1)
                    Yas = True
                elif axis_val < -0.5:
                    moveCart(i, 0)
                    Yas = True
                else:
                    Yas = False
            case 2:
                if axis_val > 0.5:
                    moveJ(i, 1)
                elif axis_val < -0.5:
                    moveJ(i, 0)
            case 3:
                if axis_val > 0.5:
                    moveJ(i, 1)
                elif axis_val < -0.5:
                    moveJ(i, 0)
            # L2 = z-as omlaag
            case 4:
                if axis_val > -0.9:
                    moveCart(i, 0)

            # R2 = z-as omhoog
            case 5:
                if axis_val > -0.9:
                    moveCart(i, 0)

    for i in range(buttons):
        button_val = joystick.get_button(i)
        if button_val:
            match i:
                case 0:
                    robot.MoveGripper(2, 100, 100, 100, 10000, 0, 0, 0, 0, 0)
                case 1:
                    robot.MoveGripper(2, 0, 100, 100, 10000, 0, 0, 0, 0, 0)
                case 15:
                    r = 425  # wanneer alles soepel werkt veranderen naar wissel tussen as 5 en as 6 (grijper)

                case 9:
                    BigMove = False
                    print("BIG MOVE FALSE")
                case 10:
                    BigMove = True
                    print("BIG MOVE TRUE")

                # gaat weg als boolean wissel tussen as 5 en 6 werkt
                case 13:
                    moveJ(i, 0)
                case 14:
                    moveJ(i, 0)


def main():
    global r, Xas, Yas, Zas
    rtn, pos = robot.GetActualTCPPose()
    r = calc.getR(pos[0], pos[1])
    while True:
        readJoystick()
        if Xas == False and Yas == False and Zas == False:
            robot.MotionQueueClear()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        robot.ResetAllError()
        robot.CloseRPC()
    finally:
        robot.ResetAllError()
        robot.CloseRPC()
