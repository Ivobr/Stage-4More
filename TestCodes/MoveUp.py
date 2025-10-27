#
# code om de juiste hoogte te krijgen voor elke grijper
# hoogte kan verschillen per grijper ontwerp
# krijg de joint_pos waarden door via SetDrag.py de arm te positioneren waarbij de grijper net niet de grond raakt
#

from fairino import Robot
import time
robot = Robot.RPC('192.168.178.23')


level = [4.0,4.0,4.0,4.0,4.0,4.0]
tool = 1
user = 0
blendT = -1
vel = 100
robot.SetSpeed(25)

robot.SetAnticollision(0, level=level, config=1)
robot.SetCollisionStrategy(3)


joint_pos = [[11.021, -134.44, -118.177, -19.874, 90, -127.14], # Pick up point + 30cm
             [-87.29,-86.502, -100.31,-31.686, 90, -45.205] # Drop point + 30 cm
]
# rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, vel=vel, user=user)

rtn, pos = robot.GetActualTCPPose()

pos[2] += 300
# rtn = robot.MoveCart(desc_pos=pos, tool=tool, vel=vel, user=user)

rtn = robot.GetActualJointPosDegree()
robot.ActGripper(2,0)
time.sleep(1)
robot.ActGripper(2,1)
time.sleep(5)
rtn = robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)

print(rtn)

