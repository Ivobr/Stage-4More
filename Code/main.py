from fairino import Robot
import time
import random

sensor = False
band = False
joint_pos = [-11.904, -99.669, 117.473, -108.616, -91.726, 74.256]  # random start position
rest_pos = [10,10,10,10,10,10]


robot = Robot.RPC('192.168.52.2')

def rest():
    if joint_pos == rest_pos:
        time.sleep(1)
    else:
        move(rest_pos)


def inputsensor():
    global sensor
    global joint_pos
    print("Reading sensor")
    # sensor.read(type shit)
    num = random.randint(1, 10)
    print(num)
    if num == 4:
        sensor = True
        joint_pos = [0, 0, 0, 0, 0, 0]  # band pos


def move(moveTo):
    global joint_pos
    global band
    print("Moving to")
    print(moveTo)
    if not band:
        print("Move to band")
        # rtn = robot.MoveJ(joint_pos=moveTo, tool=tool, user=user, exaxis_pos=epos, blendT=blendT, offset_flag=flag, offset_pos=offset_pos1)
        band = True
    else:
        print("Move to flower")
        # err, pose = robot.GetActualTCPPose(0) # pos = [x,y,z,rx,ry,rz]
        # pose[2] -= 20.0 # move down 20 mm
        # rtn = robot.MoveL(cart_pos=pose, tool=0, user=0, vel=50, acc=50)


    print("moved")
    joint_pos = moveTo

def main():
    print(joint_pos)
    while not sensor:
        rest()
        inputsensor()
    print("Done")
    move(joint_pos)


if __name__ == '__main__':
    main()
    # robot.CloseRPC()