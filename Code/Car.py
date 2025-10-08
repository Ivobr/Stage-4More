from fairino import Robot
import time
import random
# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.58.2')
joint_points = [
    [-89, -55, -0.3, -122, -92, 45],
    [-73.078, -52.969, 3.627, -50.079, -92.619, -119.16], # pickup
    [-276, 574, 709, 173, -6.95, 136.28]    # pickup xyz rx ry rz

]

drop_points = [
     [-95, -50, -0.5, -51.6, -90, -45],    # drop point 1
    [-100, -50.74, -0.42, -48.80, -88.92, -54.99], # drop point 2
    [-104, -50, -0.91, -51.7, -90, -56]    # drop point 3
]
drop_points_cords = [
    [-45, 651,706, -171, -8.53, 39.423],
    [-276, 574, 708, 173, -6,94, 136],
    [56.2, 649, 709, -172, -10,4, 41,48]
]

offset_pos = [0] * 6
epos = [0] * 4
tool = user = 0
vel = acc = ovl = 100.0
blendT = -1.0
flag = 0
robot.SetSpeed(75)
robot.ActGripper(2,0)


pick = True
dropped = 0
time.sleep(3)
robot.ActGripper(2, 1)
time.sleep(3)

def inputHandle():
    print("reading sensor")
    num = random.randint(1, 10)
    while True:
        num = random.randint(1, 10)
        if num == 4:
            break
        print(num)
        time.sleep(1)

def move(point):
    global dropped
    global pick
    if pick==True:
        # rtn = robot.MoveCart(desc_pos=point, tool=tool, user=user, blendT=blendT, vel=vel)
        rtn = robot.MoveJ(joint_pos=point, tool=tool, user=user, blendT=blendT, vel=vel)
        print(rtn)
        print("Open gripper")

        rtn =  robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
        print(rtn)
        print("Wait for closing signal")
        # text = input("Press enter to close gripper")

        robot.MoveGripper(2, 78, 100, 8, 10000, 0, 0, 0, 0, 0)
        print("Gripper closed")

        rtn, pos = robot.GetActualTCPPose()
        print(pos)
        pos[1] -= 60
        pos[2] += 40
        print(pos)
        rtn = robot.MoveCart(desc_pos=pos, tool=tool, user=user, blendT=blendT)
        print(rtn)

        pick = False
    else:
        # rtn = robot.MoveJ(joint_pos=point,tool=tool,user=user,vel=vel)
        rtn = robot.MoveCart(desc_pos=point, tool=tool, user=user, blendT=blendT, vel=vel)
        print(rtn)
        rtn = robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
        print(rtn)
        rtn, pos = robot.GetActualTCPPose()
        print(pos)
        pos[1] -= 60
        pos[2] += 40
        print(pos)
        rtn = robot.MoveCart(desc_pos=pos, tool=tool, user=user, blendT=blendT)
        print("Move Cart return", rtn)
        pos = robot.GetActualTCPPose()
        print(pos)
        dropped = dropped + 1
        pick = True


inputHandle()
move(joint_points[1])
print("Move to drop point")
print(dropped, "Dropped now before doing it")
move(drop_points_cords[dropped])
print("Dropped: ", dropped)
move(joint_points[1])
move(drop_points_cords[dropped])
print("Dropped: ", dropped)
move(joint_points[1])
move(drop_points_cords[dropped])
print("Dropped: ", dropped)
robot.CloseRPC()


