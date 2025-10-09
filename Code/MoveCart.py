from fairino import Robot
import time

robot = Robot.RPC('192.168.58.2')

cords = [
    # 375 -> -275
    [-275, 574, 708, 173, -6.94, 136],
    [-45, 651,706, -171, -8.53, 39.423],
    [7.62, 642, 708, -173, -7.55, 44.8],
    [56.2, 649, 709, -172, -10.4, 41.48],
    [375, -532, 709, -172, -10.4, -98]
]

# basic setup
tool = user = 0
blendT = -1.0
flag = 0


rtn, pos = robot.GetActualTCPPose()
print("before +20",pos)
pos[2] += 200
rtn = robot.MoveCart(desc_pos=pos, tool=tool, user=user, blendT=blendT)
print(rtn)
print("\n")

rtn, pos = robot.GetActualTCPPose();
print("After +20",pos)
print("\n")

rtn, pos = robot.GetActualJointAccDegree()
print("Before turingin gripper",pos)
print("\n")
pos[5] += 20
rtn = robot.MoveJ(joint_pos=pos, tool=tool, user=user, blendT=blendT)
print(rtn)
print(robot.GetActualJointAccDegree())
print("\n")


rtn, pos = robot.GetActualTCPPose();
print("After j6 turned", pos)


