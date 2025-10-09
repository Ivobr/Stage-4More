from fairino import Robot
import time

robot = Robot.RPC('192.168.58.2')
robot.ActGripper(2,0)
time.sleep(1)
robot.ActGripper(2, 1)
time.sleep(1)

cords = [
    # 375 -> -275
    [625, 4.438, -32.246, -179, -0.404, 41.868], # pickup point
    [-76.302, -472.35, 123.296, -179.11, -1.699, -40.09], # drop point
]

# basic setup
tool = user = 0
blendT = -1.0
flag = 0

robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
cords[0][2]+=300
robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)
cords[0][2]-=300
robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)

robot.MoveGripper(2, 78, 100, 8, 10000, 0, 0, 0, 0, 0)

cords[0][2]+=300
robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)

cords[1][2]+=300
robot.MoveCart(desc_pos=cords[1], tool=tool, blendT=blendT, user=user)
cords[1][2]-=300
robot.MoveCart(desc_pos=cords[1], tool=tool, blendT=blendT, user=user)
robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)

cords[1][2]+=300
robot.MoveCart(desc_pos=cords[1], tool=tool, blendT=blendT, user=user)
