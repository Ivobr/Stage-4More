from numpy.f2py.auxfuncs import throw_error

from fairino import Robot
import pygame
import time
import math

vel = 100
user = 0
tool = 0

input = False
BigMove = False

BigMovement = 50
SmallMovement = 1

BigMovementA = 5
SmallMovementA = 0.5

r = 425

takeNeg = False
yNeg = False


pygame.init()
pygame.joystick.init()

robot = Robot.RPC('192.168.178.23')

robot.ActGripper(2,0)
time.sleep(1)
rtn = robot.ActGripper(2,1)
time.sleep(3)
print(rtn)
joystick = pygame.joystick.Joystick(0)
joystick.init()

def getR(x, y):
    global r
    x *= x
    y *= y
    r2 = x + y
    r = math.sqrt(r2)

def calcPoint(x, r):
    global takeNeg
    global yNeg
    print("takeNeg = ", takeNeg, " yNeg = ", yNeg, " x = ", x, " r = ", r)
    # in deze functie wordt de waarden van y berekent als er een nieuwe x waarde is
    if x > r:
        takeNeg = not takeNeg
        yNeg = not yNeg
        return False
    elif x < -r:
        takeNeg = not takeNeg
        yNeg = not yNeg
        return False
    x *= x
    r *= r
    y2 = r - x
    y = math.sqrt(y2)
    if takeNeg:
        y = -y
        return y
    else:
        return y



def moveCart(axis, value):
    match axis:
        case 0:
            rtn, pos = robot.GetActualTCPPose()
            if value == 1:
                if BigMove:
                    pos[0] += BigMovement
                    calcPoint(pos[0], r)
                    pos[1] = calcPoint(pos[0], r)
                    if calcPoint(pos[0], r) == False:
                        return
                else:
                    pos[0] += SmallMovement
                    calcPoint(pos[0], r)
                    pos[1] = calcPoint(pos[0], r)
                    if calcPoint(pos[0], r) == False:
                        return
                rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool)
                print(rtn, pos)
            elif value == 0:
                if BigMove:
                    pos[0] -= BigMovement
                    calcPoint(pos[0], r)
                    pos[1] = calcPoint(pos[0], r)
                else:
                    pos[0] -= SmallMovement
                    calcPoint(pos[0], r)
                    pos[1] = calcPoint(pos[0], r)
                rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool)
                print(rtn, pos)
        case 1:
            rtn, pos = robot.GetActualTCPPose()
            if value == 1:
                if BigMove:
                    pos[1] += BigMovement
                else:
                    pos[1] += SmallMovement
                rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool)
                print(rtn, pos)
            elif value == 0:
                if BigMove:
                    pos[1] -= BigMovement
                else:
                    pos[1] -= SmallMovement
                rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool)
                print(rtn, pos)
        case 4:
            rtn, pos = robot.GetActualTCPPose()
            if BigMove:
                pos[2] -= BigMovement
            else:
                pos[2] -= SmallMovement
            rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool)
        case 5:
            rtn, pos = robot.GetActualTCPPose()
            if BigMove:
                pos[2] += BigMovement
            else:
                pos[2] += SmallMovement
            rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool)



    print("Moving cart...")


    #functie om de kop van de arm aan te sturen
def moveJ(axis, value):
    match axis:
        case 2:
            #stuur Joint 5 aan
            print(value)
            if value == 1:
                rtn, pos = robot.GetActualJointPosDegree()
                if BigMove:
                    pos[4] += BigMovementA
                else:
                    pos[4] += SmallMovementA
                robot.MoveJ(pos, vel=vel, user=user, tool=tool)
            elif value == 0:
                rtn, pos = robot.GetActualJointPosDegree()
                if BigMove:
                    pos[4] -= BigMovementA
                else:
                    pos[4] -= SmallMovementA
                robot.MoveJ(pos, vel=vel, user=user, tool=tool)
        case 3:
            # stuur Joint 4 aan
            print(value)
            if value == 1:
                rtn, pos = robot.GetActualJointPosDegree()
                if BigMove:
                    pos[3] += BigMovementA
                else:
                    pos[3] += SmallMovementA
                robot.MoveJ(pos, vel=vel, user=user, tool=tool)
            elif value == 0:
                rtn, pos = robot.GetActualJointPosDegree()
                if BigMove:
                    pos[3] -= BigMovementA
                else:
                    pos[3] -= SmallMovementA
                robot.MoveJ(pos, vel=vel, user=user, tool=tool)


        case 13:
            rtn, pos = robot.GetActualJointPosDegree()
            if BigMove:
                pos[5] -= BigMovementA
            else:
                pos[5] -= SmallMovementA
            robot.MoveJ(pos, vel=vel, user=user, tool=tool)
        case 14:
            rtn, pos = robot.GetActualJointPosDegree()
            if BigMove:
                pos[5] += BigMovementA
            else:
                pos[5] += SmallMovementA
            robot.MoveJ(pos, vel=vel, user=user, tool=tool)



# rtn, pos = robot.GetActualTCPPose()
# getR(pos[0], pos[1])
# lees controller input
running = True
while running:
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
                    if yNeg:
                        moveCart(i, 0)
                    else:
                        moveCart(i, 1)
                elif axis_val < -0.5:
                    if yNeg:
                        moveCart(i, 1)
                    else:
                        moveCart(i, 0)
            case 1:
                if axis_val > 0.5:
                    moveCart(i, 1)
                elif axis_val < -0.5:
                    moveCart(i, 0)
            case 2:
                if axis_val > 0.5:
                    moveJ(i, 1)
                elif axis_val < -0.5:
                    moveJ(i, 0)
            case 3:
                if axis_val > 0.5:
                    moveJ(i,1)
                elif axis_val < -0.5:
                    moveJ(i,0)
            # L2 = z-as omlaag
            case 4:
                if axis_val > -0.9:
                    moveCart(i, 0)

            # R2 = z-as omhoog
            case 5:
                if axis_val > -0.9:
                    moveCart(i,0)




    for i in range(buttons):
        button_val = joystick.get_button(i)
        if button_val:
            match i:
                case 0:
                    robot.MoveGripper(2, 100, 100, 100, 10000,0,0,0,0, 0)
                case 1:
                    robot.MoveGripper(2, 0, 100, 100, 10000, 0, 0, 0, 0, 0)




                case 9:
                    BigMove = False
                    print("BIG MOVE FALSE")
                case 10:
                    BigMove = True
                    print("BIG MOVE TRUE")


                case 13:
                    moveJ(i, 0)
                case 14:
                    moveJ(i,0)
    if input == True:
        time.sleep(0.5)
        input = False