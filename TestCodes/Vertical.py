from fairino import Robot
import time

robot = Robot.RPC('192.168.178.23')


level = [4.0,4.0,4.0,4.0,4.0,4.0]
tool = 1
user = 0
blendT = -1
vel = 100

robot.SetAnticollision(0, level=level, config=1)
robot.SetCollisionStrategy(3)


joint_pos = [[11.020, -99.623, -109.587, -63.589, 90, -127], # Pick up point + 30cm
             [-87.29,-86.502, -100.31,-31.686, 90, -45.205] # Drop point + 30 cm
]

robot.ActGripper(2,0)
time.sleep(1)
robot.ActGripper(2,1)
time.sleep(3)




rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, user=user, vel=vel)
robot.MoveGripper(2, 0, 100, 100, 10000, 0, 0, 0, 0, 0)

rtn, pos = robot.GetActualTCPPose()
pos[2] = pos[2] - 300

rtn = robot.MoveCart(pos, tool, user, vel)
print(rtn)

time.sleep(2)
robot.MoveGripper(2, 100, 100, 100, 10000, 0, 0, 0, 0, 0)

time.sleep(2)
rtn, pos = robot.GetActualTCPPose()
pos[2] = pos[2] + 300

rtn = robot.MoveCart(pos, tool, user, vel)
print(rtn)
time.sleep(2)

robot.MoveJ(joint_pos=joint_pos[1], tool=tool, user=user, vel=vel)


robot.MoveGripper(2, 0, 100, 100, 10000, 0, 0, 0, 0, 0)


time.sleep(1)
robot.ResetAllError()


rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, user=user, vel=vel)
