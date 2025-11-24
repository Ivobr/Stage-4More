import time
import pygame
import calc
from fairino import Robot

robot = Robot.RPC('192.168.178.23')

joystick = 0

acc = 20
user = 0
tool = 0
vel = 100
pos = []

r = 0
a = 0

lastValX = lastValY = lastValZup = lastValZdown = lastValS5 = lastValS4 = 0

# bewegingen booleans
Rotation = False
incr = False
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
    # Noodstop voor de controller
    robot.StopMotion()
    robot.DragTeachSwitch(1)
    time.sleep(5)
    robot.DragTeachSwitch(0)


def IncreaseR(axis_val, direction):
    global a
    stopped = False
    rtn, pos = robot.GetActualTCPPose()
    r = calc.getR(pos[0], pos[1])

    step = axis_val * 20  # bigger multiplier = faster
    r += step if direction else -step

    Nx, Ny = calc.increaseR(r, a)

    target = [Nx, Ny, pos[2], pos[3], pos[4], pos[5]]

    # Stream continuously
    robot.ServoCart(
        mode=0,
        desc_pos=target,
        pos_gain=[1, 1, 1, 0, 0, 0],
        vel=100,
        acc=100
    )


def JOG(number, direction, axis_val):
    global gripper, stopped
    stopped = False
    robot.StopJOG(3)
    # little sleep to reset
    time.sleep(0.1)
    if number == 2:
        vel = (axis_val * 100) / 2
        print("Speed for ax 4 and 5 ", vel)
        rtn = robot.StartJOG(ref=2, nb=3, dir=direction,
                             max_dis=10000, vel=vel)
    elif number == 5:
        vel = (axis_val * 100)
        print("New speed ", vel)
        if gripper:
            rtn = robot.StartJOG(ref=0, nb=6, dir=direction,
                                 max_dis=10000, vel=vel)
        else:
            rtn = robot.StartJOG(
                ref=0, nb=number, dir=direction, max_dis=10000, vel=vel)
    else:
        vel = (axis_val * 100)
        print("New speed ", vel)
        rtn = robot.StartJOG(
            ref=0, nb=number, dir=direction, max_dis=10000, vel=vel)
    print(rtn)


def readJoystick():
    global joystick, a, Rotation, incr, ZasDown, ZasUp, S5, S4, lastValX, lastValY, lastValZdown, lastValZup, lastValS4, lastValS5, gripper, stopped
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
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        print(axis_val)
                        JOG(1, 1, axis_val)
                        lastValX = axis_val
                    Rotation = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValX > 0.1 or axis_val - lastValX < -0.1:
                        JOG(1, 0, axis_val)
                        lastValX = axis_val
                    Rotation = True
                else:
                    Rotation = False
            case 1:
                if not incr:
                    rtn, pos = robot.GetActualTCPPose()
                    a = calc.getA(pos[0], pos[1])
                    robot.ServoMoveStart()
                if axis_val > 0.1:
                    IncreaseR(axis_val, 0)
                    incr = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    IncreaseR(axis_val, 1)
                    incr = True
                else:
                    incr = False
                    rtn, pos = robot.GetActualTCPPose()
                    robot.ServoCart(
                        mode=0,
                        desc_pos=pos,
                        pos_gain=[0, 0, 0, 0, 0, 0],  # no movement
                        vel=0,
                        acc=0
                    )
                    robot.ServoMoveEnd()
                    robot.StopMotion()
                    robot.MotionQueueClear()
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
                case 5:
                    print("Noodknop functie")
                    stop()
                case 15:
                    gripper = not gripper
                    robot.SetDO(0, gripper)
                    time.sleep(1)


def main():
    global r, a, Rotation, incr, ZasDown, ZasUp, S4, S5, stopped
    print("Main")

    setup()
    while True:
        readJoystick()
        if Rotation == False and ZasDown == False and ZasUp == False and S4 == False and S5 == False and stopped == False:
            print("In if statement")
            robot.ServoMoveEnd()
            robot.StopJOG(3)
            robot.StopMotion()
            robot.MotionQueueClear()
            print(robot.GetMotionQueueLength())
            print(robot.GetMotionQueueLength())
            stopped = True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        robot.CloseRPC()
        print("Stopped")
