import time

from fairino import Robot

robot = Robot.RPC('192.168.178.23')

joint_pos = [[6.021, -111.91, -95.496, -63.832, 90, -127.14], [-87.29, -86.502, -100.31, -83.686, 90, -132.205]]

tool = 0
user = 0
vel = 100.0

level = [4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
mode = 0
config = 1
speed = 25

rtn = robot.SetSpeed(speed)

rtn = robot.SetAnticollision(mode=mode, level=level, config=config)
print(rtn)

rtn = robot.SetCollisionStrategy(3, 2000, 100, 250)
print(rtn)

time.sleep(5)
rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, user=user, vel=vel)
print(rtn)

rtn = robot.MoveJ(joint_pos=joint_pos[1], tool=tool, user=user, vel=vel)
print(rtn)

rtn, pos = robot.GetActualTCPPose()
pos[2] += 300
rtn = robot.MoveCart(desc_pos=pos, tool=tool, user=user, vel=vel)

rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, user=user, vel=vel)
print(rtn)

robot.CloseRPC()
