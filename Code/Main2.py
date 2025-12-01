#
# Compleet functionerende controller code
# Er wordt een queue gecheckt voor er nieuwe cords worden gestuurt
# Het is eigenlijk combined.py met meer comments
#

from fairino import Robot
import time
import calc
import pygame

# pygame
joystick = 0

# variable
tool = 0
user = 0
vel = 0
blendT = 1
count = 0

# coordinates
# [[pick-up area],[drop area]]
j_pos = [[87.29, -120.27, -91.78, -58.19, 90, 58],
         [91.606, -49.13, 66.899, -105.166, -90, 58]
         ]
pos = []  # huidige positie
r = 0  # Radius
a = 0  # Hoek

# veiligheids variabele
secure = [4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
mode = 0
config = 1
slowing = False

# bewegings booleans
lastValRot = lastValRotInc = lastValZup = lastValZdown = lastValS4 = lastValS5 = 0
Rotation = False
RotationInc = False
ZasUp = False
ZasDown = False
S4 = False
S5 = False
stopped = False
# Boolean om de grijper te selecteren
gripper = False

# robot verbinden
robot = Robot.RPC('192.168.178.23')


def setup():
    global joystick, r, a, pos

    print("Starting setup")

    # Reken huidige waardes van de straal en hoek tenopzichte van het middenpunt
    rtn, pos = robot.GetActualTCPPose()
    r = calc.getR(pos[0], pos[1])
    a = calc.getA(pos[0], pos[1])

    # initalizeer controller
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Reset en activeer grijper
    robot.ActGripper(2, 0)
    time.sleep(1)
    robot.ActGripper(2, 1)
    time.sleep(2)

    # veiligheids functies
    rtn = robot.SetAnticollision(mode, secure, config)
    print("SetAnticollosion: ", rtn)
    rtn = robot.SetCollisionStrategy(3, 2000, 100, 250)
    print("SetCollisionStrategy: ", rtn)

    print("Setup done")


def stop():
    # Zet de arm voor 5 seconden in een staat waarbij die handmatig verplaatst kan worden.
    # Ook stopt de arm gelijk met bewegen
    robot.StopMotion()
    robot.DragTeachSwitch(1)
    time.sleep(5)
    robot.DragTeachSwitch(0)


def ServoCart(axis_val, direction):
    global r, a, count

    # Zorgt ervoor dat de queue niet te lang wordt en de arm gelijk stopt bij het loslaten van de controller
    rtn, size = robot.GetMotionQueueLength()
    if count > 3:
        if size < 2:
            count = 0
        return
    rtn, pos = robot.GetActualTCPPose()
    r = calc.getR(pos[0], pos[1])
    step = axis_val * 5
    r += step if direction else -step

    x, y = calc.increaseR(r, a)
    pos[0] = x
    pos[1] = y

    rtn = robot.ServoCart(mode=0, desc_pos=pos, pos_gain=[
        1, 1, 1, 0, 0, 0], vel=100, acc=100)
    count += 1


def JOG(number, direction, axis_val):
    global gripper, stopped
    print(number, axis_val)
    stopped = False
    robot.StopJOG(3)
    # Kleine sleep zodat alles echt stopt
    time.sleep(0.1)

    # L2 en R2 -> z-as
    if number == 2:
        vel = (axis_val * 100) / 2
        robot.StartJOG(ref=2, nb=3, dir=direction, max_dis=10000, vel=vel)

    # De motoren welke direct worden gestuurt
    else:
        vel = (axis_val * 100)
        if gripper and number == 5:
            robot.StartJOG(ref=0, nb=6, dir=direction, max_dis=10000, vel=vel)
        else:
            robot.StartJOG(ref=0, nb=number, dir=direction,
                           max_dis=10000, vel=vel)


def readJoystick():
    global slowing, joystick, Rotation, RotationInc, ZasUp, ZasDown, S4, S5, lastValRot, lastValRotInc, lastValZup, lastValZdown, lastValS4, lastValS5, gripper
    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return

    # uitlezen joysticks
    for i in range(axes):
        axis_val = joystick.get_axis(i)
        match i:
            case 0:
                if axis_val > 0.1:
                    if axis_val - lastValRot > 0.1 or axis_val - lastValRot < -0.1:
                        # Nog eff checken of die niet de andere kant op moet
                        JOG(1, 1, axis_val)
                        lastValRot = axis_val
                    Rotation = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    if axis_val - lastValRot > 0.1 or axis_val - lastValRot < -0.1:
                        # Nog eff checken of die niet de andere kant op moet
                        JOG(1, 0, axis_val)
                        lastValRot = axis_val
                    Rotation = True
                else:
                    Rotation = False
            case 1:
                if not RotationInc:
                    robot.ServoMoveStart()
                if axis_val > 0.1:
                    ServoCart(axis_val, 0)
                    RotationInc = True
                elif axis_val < -0.1:
                    axis_val = abs(axis_val)
                    ServoCart(axis_val, 1)
                    RotationInc = True
                else:
                    # Benodigdheid hiervan eff snel testen
                    RotationInc = False
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
                # as 5 en grijper
                # Hier is de axis_val beginpunt 0.2 ivm dat als de linker joystick wordt gebruikt de rechter joystick nog beetje beweegt
                # Krijg je van een oude controller
                if axis_val > 0.2:
                    if axis_val - lastValS5 > 0.1 or axis_val - lastValS5 < -0.1:
                        JOG(5, 0, axis_val)
                        lastValS5 = axis_val
                    S5 = True
                elif axis_val < -0.2:
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
                # L and R2 hebben een standaardt waarden van -1.0 ipv 0.0 dus door er +1 bij te doen wordt dit gelijk getrokken
                axis_val += 1
                if axis_val > 0.1:
                    rtn, pos = robot.GetActualTCPPose()
                    print("Pos ", pos[2])
                    rtn, speed = robot.GetTargetTCPSpeed()
                    print("Speed ", speed[2])
                    if pos[2] < 150 and speed[2] < -200:
                        robot.StopJOG(3)
                        time.sleep(1)
                        JOG(2, 0, 0.25)
                        # robot.ImmStopJOG()
                    elif pos[2] < -20:
                        robot.ImmStopJOG()
                    elif axis_val - lastValZdown > 0.2 or axis_val - lastValZdown < -0.2 and slowing == False:
                        JOG(2, 0, axis_val)
                        lastValZdown = axis_val
                    ZasDown = True
                else:
                    ZasDown = False
                    slowing = False
            case 5:
                axis_val += 1
                if axis_val > 0.1:
                    rtn, pos = robot.GetActualTCPPose()
                    print("Pos ", pos[2])
                    if pos[2] > 400:
                        robot.StopJOG(3)
                    elif axis_val - lastValZup > 0.2 or axis_val - lastValZup < -0.2:
                        JOG(2, 1, axis_val)
                        lastValZup = axis_val
                    ZasUp = True
                else:
                    ZasUp = False

    # uitlezen buttons
    for i in range(buttons):
        button = joystick.get_button(i)
        if button:
            match i:
                case 0:
                    # Open de grijper 1 mm veder zodat er minder druk op de grijper, maar de bloem blijft stevig zitten.
                    # Kijken of dit echt werkt en welke andere manieren er zijn om minder druk op de grijper te krijgen
                    robot.MoveGripper(2, 100, 100, 1, 5000, 1, 0, 0, 0, 0)
                    time.sleep(1.5)
                    rtn, err, pos = robot.GetGripperCurPosition()
                    print(pos)
                    pos -= 1
                    robot.MoveGripper(2, pos, 100, 1, 5000, 1, 0, 0, 0, 0)

                case 1:
                    robot.MoveGripper(2, 0, 100, 1, 5000, 1, 0, 0, 0, 0)

                case 2:
                    # moveJ naar pick-up area
                    robot.MoveJ(joint_pos=j_pos[0],
                                tool=tool, user=user, vel=50)

                case 3:
                    # moveJ naar drop area
                    robot.MoveJ(joint_pos=j_pos[1],
                                tool=tool, user=user, vel=50)

                case 5:
                    print("NoodKnop")
                    stop()

                case 15:
                    # Gebruik deze knop om te wisselen tussen motor as 5 en de grijper
                    gripper = not gripper
                    robot.SetDO(0, gripper)
                    time.sleep(1)


def main():
    global a, stopped, Rotation, RotationInc, ZasDown, ZasUp, S4, S5
    setup()

    while True:
        readJoystick()
        # Als alle bewegingen False zijn wordt de beweging compleet gestopt
        if Rotation == False and RotationInc == False and ZasDown == False and ZasUp == False and S4 == False and S5 == False and stopped == False:
            rtn = robot.StopJOG(3)
            rtn = robot.ServoMoveEnd()
            # Als er een limit error is wordt deze weg gehaald want ServoMoveEnd geeft ook de limit errors terug
            if rtn == 14:
                print("Een limit", rtn)
                rtn = robot.ResetAllError()
                print(rtn)
            rtn = robot.StopMotion()
            rtn = robot.MotionQueueClear()
            stopped = True
            rtn, pos = robot.GetActualTCPPose()
            a = calc.getA(pos[0], pos[1])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        robot.CloseRPC()
        print("Connection closed")
