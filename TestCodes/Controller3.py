import time

import pygame

from fairino import Robot

robot = Robot.RPC('192.168.178.23')

joystick = 0

user = 0
tool = 0
blendT = 500
vel = 100


# bewegingen booleans


def setup():
    global joystick

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


def readJoystick():
    global joystick
    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()

    for i in range(axes):
        axis_val = joystick.get_axis(i)


def main():
    print("Main")

    # setup()
    while True:
        # do shit
        readJoystick()
        print("shit doen")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        robot.CloseRPC()
