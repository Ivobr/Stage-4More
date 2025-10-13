from fairino import Robot
import time

sensor = False
band = False
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

# set up main for test plan setup
robot = Robot.RPC('192.168.52.2')
def setup():
    # Reset gripper om er zeker van te zijn dat die werkt
    # Zorg dat niks tussen de vingers zit het 0 en 100 punt wordt bepaald

    robot.ActGripper(2,0) # verander 2 naar coresponding index
    time.sleep(1)
    robot.ActGripper(2,1)
    time.sleep(1)




def inputsensor():
    global sensor
    rtn, status = robot.GetDI(0) # juiste pin invullen
    if status:
        sensor = True

def moveGripper(pos):
    rtn = robot.MoveGripper(2, pos, 100, 8, 10000, 0, 0, 0, 0, 0)
    print("Moving gripper: ", rtn)

def move(moveTo, dif):
    global joint_pos
    global band
    print("Moving to")
    print(moveTo)
    if moveTo != 0:
        rtn = robot.MoveJ(joint_pos=moveTo, tool=tool, vel=vel, user=user, blendT=blendT)
        print("MoveJ: ", rtn)
    elif moveTo == 0:
        rtn, pos = robot.GetActualTCPPose()
        pos[2] = pos[2] + dif
        rtn = robot.MoveCart(desc_pos=pos, vel=vel, user=user, blendT=blendT)
        print("MoveCart: ", rtn)
    rtn = robot.GetActualTCPPose()
    print("moved", rtn)

def main():
    moveGripper(0)
    while not sensor:
        inputsensor()

    move(joint_pos[0], 0)
    moveGripper(0)
    print("Wait a sec")
    time.sleep(1)

    # zet moveTo als 0 om de lineare bewiging te gebruiken
    move(0, -30)
    moveGripper(78)
    move(0, 30)
    move(joint_pos[2], 0)
    move(0, -30)
    moveGripper(0)
    move(0, 30)
    move(joint_pos[0], 0)

if __name__ == '__main__':
    main()
    # robot.CloseRPC()