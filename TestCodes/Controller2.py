from TestCodes.ControllerMove import BigMovement
from fairino import Robot
import time
import pygame
import calc

robot = Robot.RPC('192.168.178.23')

x, y, r, a = 0

BigMove = False
BigMovement = 50
BigMovementA = 5

SmallMovement = 5
SmallMovementA = 0.5

takeNeg = False
xOpp = False

vel = 100
user, tool = 0

joystick = 0

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
    global x, y, r, a, takeNeg, xOpp

    rtn, pos = robot.GetActualTCPPose()

    # update de waarden van r en a voor als deze gewijzigt zijn
    r = calc.getR(pos[0],pos[1])
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
                    pos [1] = calc.calcPoint(pos[0], r, takeNeg)
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
            rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool)
        case 1:
            a = calc.getA(pos[0],pos[1])
            r = calc.getR(pos[0, pos[1]])
            if direction:
                if BigMove:
                    r += BigMovement
                else:
                    r += SmallMovement
                x, y = calc.rIncrement(r, a)
                pos[0] = x
                pos[1] = y
            else:
                if BigMove:
                    r -= BigMovement
                else:
                    r -= SmallMovement
                x, y = calc.rIncrement(r, a)
                pos[0] = x
                pos[1] = y
            print(x,y)
            rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, tool=tool)

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
                pos[5] -=SmallMovementA
            robot.MoveJ(joint_pos=pos, vel=vel, user=user, tool=tool)
            print("14")





def readJoystick():
    global joystick
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
                    else:
                        moveCart(i, 1)
                elif axis_val < -0.5:
                    if xOpp:
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
                case 15:
                    r = 425



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


def main():
    global r
    rtn, pos = robot.GetActualTCPPose()
    r = calc.getR(pos[0], pos[1])
    while True:
        readJoystick()

if __name__ == "__main__":
    main()
