from fairino import Robot
import time

state = False
joint_pos = [[9.724, -112.39, -94.249, -63.036, 90, -122.14], # Pick up point + 30cm
             [-87.29,-86.502, -101.31,-81.686,91.851,-137.205] # Drop point + 30 cm
]

# declaratie.
offset_pos = [0] * 6
epos = [0] * 4
tool = user = 0
vel = acc = ovl = 100.0
blendT = -1.0
flag = 0

# Safety settings
secure = [4.0,4.0,4.0,4.0,4.0,4.0]
mode = 0
config = 1

# set up main for test plan setup
robot = Robot.RPC('192.168.178.23')
def setup():

    # zet safety instellingen zodat bij contact de arm stopt
    rtn = robot.SetAnticollision(mode, secure, config)
    print(rtn)

    rtn = robot.SetCollisionStrategy(3, 2000, 100, 250)
    print(rtn)

    # Reset gripper om er zeker van te zijn dat die werkt
    # Zorg dat niks tussen de vingers zit het 0 en 100 punt wordt bepaald
    robot.ActGripper(2,0) # verander 2 naar aangesloten index
    time.sleep(1)
    robot.ActGripper(2,1)
    time.sleep(1)




def inputsensor():
    global state
    rtn, state = robot.GetDI(1) # juiste pin invullen
    if state:
        state = True

def moveGripper(pos, force):
    rtn = robot.MoveGripper(2, pos, 100, force, 10000, 0, 0, 0, 0, 0)
    print("Moving gripper: ", rtn)
    time.sleep(1)

def move(moveTo, dif):
    if moveTo != 0:
        print("Moving to")
        print(moveTo)
        rtn = robot.MoveJ(joint_pos=moveTo, tool=tool, vel=vel, user=user, blendT=blendT)
        print("MoveJ: ", rtn)
    elif moveTo == 0:
        print("Changing z-axis by: ", dif)
        rtn, pos = robot.GetActualTCPPose()
        pos[2] = pos[2] + dif
        print(pos)
        time.sleep(2)
        rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, blendT=blendT, tool=tool)
        print("MoveCart: ", rtn)
    rtn = robot.GetActualTCPPose()
    print("moved", rtn)

def main():
    moveGripper(0, 100)
    while state == False:
        inputsensor()

    # ga naar band als die daar niet al is en open grijper
    move(joint_pos[0], 0)
    moveGripper(0, 100)
    time.sleep(1)

    # zet moveTo als 0 om de lineare bewiging te gebruiken

    # Ga omlaag en pak object en ga weer omhoog
    move(0, -300)
    moveGripper(100, 100)
    move(0, 300)
    time.sleep(1)

    # ga naar drop punt
    move(joint_pos[1], 0)
    time.sleep(1)

    # ga omlaag en leg neer ga weer omhoog
    move(0, -300)
    moveGripper(0, 100)
    move(0, 300)
    time.sleep(1)

    # ga terug naar band
    move(joint_pos[0], 0)

if __name__ == '__main__':
    setup()
    main()
    time.sleep(3)
    robot.ResetAllError()
    robot.CloseRPC()