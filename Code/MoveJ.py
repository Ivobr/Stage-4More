from fairino import Robot
import time

robot = Robot.RPC('192.168.58.2')
robot.ActGripper(2,0)
time.sleep(1)
robot.ActGripper(2, 1)
time.sleep(1)

joint_pos = [
    [7.43, -140.98, -101.84, -26.03, 87.57, -100.27],
    [-80.15, -109.48, -126.80, -33.68, 91.28, -124],
    [-95, -50, -0.5, -51.6, -90, -45]
]


# basic setup
vel = acc = ovl = 100
tool = user = 0
blendT = -1.0
robot.SetSpeed(50)

rtn, pos = robot.GetActualTCPPose()

print(pos)
pos[2] += 300
print(pos)
rtn = robot.MoveCart(desc_pos=pos, tool=tool, user=user, blendT=blendT)
print(rtn)

robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)

rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, blendT=blendT, vel=vel, user=user)
print(rtn)
robot.MoveGripper(2, 78, 100, 8, 10000, 0, 0, 0, 0, 0)

rtn, pos = robot.GetActualTCPPose()

print(pos)
pos[2] += 300
print(pos)
rtn = robot.MoveCart(desc_pos=pos, tool=tool, user=user, blendT=blendT)
print(rtn)

rtn = robot.MoveJ(joint_pos=joint_pos[1], tool=tool, blendT=blendT, vel=vel, user=user)
robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)

rtn, pos = robot.GetActualTCPPose()
print(pos)
pos[2] += 300
print(pos)
rtn = robot.MoveCart(desc_pos=pos, tool=tool, user=user, blendT=blendT)
print(rtn)

rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, blendT=blendT, vel=vel, user=user)
print(rtn)