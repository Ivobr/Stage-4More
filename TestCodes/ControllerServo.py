import time

import pygame

import calc
from fairino import Robot

# *
# Soepele bewegingen alleen rotatieas vergroten werkt traag en zonder snelheid variabele
#   ServoCart werkt soort van hij schokt terug naar de plek waar je hem hebt losgelaten
#   Je kan niet sneller/langzamer of in grotere/kleinere stappen bewegen
# Alle andere bewegingen hebben een variabele snelheid.
#
#
# Gebruikt in testplan voor de test:
#   Vloeiende beweging Code 1*#
robot = Robot.RPC('192.168.178.23')

joystick = 0

acc = 20
user = 0
tool = 0
blendT = 1
vel = 100
pos = []

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


def stop():
    robot.StopMotion()
    robot.DragTeachSwitch(1)
    time.sleep(5)
    robot.DragTeachSwitch(0)


def IncreaseR(axis_val, direction):
    step = axis_val * 5
    r += step if direction else -step

    Nx, Ny = calc.increaseR(r, a)

    target = [Nx, Ny, pos[2], pos[3], pos[4], pos[5]]

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
    # Kleine slaap om daadwerkelijk te stoppen
    time.sleep(0.1)
    if number == 2:
        vel = (axis_val * 100) / 2
        print("Speed for ax 4 and 5 ", vel)
        rtn = robot.StartJOG(ref=2, nb=3, dir=direction,
                             max_dis=10000, vel=vel)
    elif number == 5:
        vel = (axis_val * 100)
        if gripper:
            rtn = robot.StartJOG(ref=0, nb=6, dir=direction,
                                 max_dis=10000, vel=vel)
        else:
            rtn = robot.StartJOG(
                ref=0, nb=number, dir=direction, max_dis=10000, vel=vel)
    else:
        vel = (axis_val * 100)
        rtn = robot.StartJOG(
            ref=0, nb=number, dir=direction, max_dis=10000, vel=vel)
    print(rtn)


def readJoystick():
    global joystick, Xas, Yas, ZasDown, ZasUp, S5, S4, lastValX, lastValY, lastValZdown, lastValZup, lastValS4, lastValS5, gripper, stopped
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
                if not Yas:
                    robot.ServoMoveStart()
                if axis_val > 0.1:
                    IncreaseR(axis_val, 0)
                    Yas = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    IncreaseR(axis_val, 1)
                    Yas = True
                else:
                    # Benodigdheid hiervan eff snel testen
                    Yas = False
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
                    # Open de grijper 1 mm veder zodat er minder druk op de grijper, maar de bloem blijft stevig zitten.
                    robot.MoveGripper(2, 100, 100, 1, 5000, 1, 0, 0, 0, 0)
                    time.sleep(2)
                    rtn, err, pos = robot.GetGripperCurPosition()
                    print(pos)
                    pos -= 1
                    robot.MoveGripper(2, pos, 100, 1, 5000, 1, 0, 0, 0, 0)
                case 1:
                    robot.MoveGripper(2, 0, 100, 1, 5000, 1, 0, 0, 0, 0)
                case 5:
                    print("Noodknop functie")
                    stop()
                case 2:
                    IncreaseR(0, 1)
                case 3:
                    IncreaseR(0, 0)
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
        if Xas == False and ZasDown == False and ZasUp == False and S4 == False and S5 == False and stopped == False:
            robot.ServoModeEnd()
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
