import time

from fairino import Robot

# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.178.23')
j1 = [-11.904, -99.669, 117.473, -108.616, -91.726, 74.256]
j5 = [-95.228, -54.621, 73.691, -112.245, -91.280, 74.268]
desc_pos1 = [-419.524, -13.000, 351.569, -178.118, 0.314, 3.833]
desc_pos5 = [-33.421, 732.572, 275.103, -177.907, 2.709, -79.482]
offset_pos = [0, 0, 0, 0, 0, 0]
epos = [0, 0, 0, 0]
tool = 0
user = 0
vel = 100.0
acc = 100.0
ovl = 100.0
blendT = -1.0
flag = 0
robot.SetSpeed(20)
rtn = robot.MoveJ(joint_pos=j1, tool=tool, user=user, vel=vel)
rtn = robot.MoveJ(joint_pos=j5, tool=tool, user=user, vel=vel, blendT=1)
time.sleep(1)
robot.PauseMotion()
time.sleep(1)
robot.ResumeMotion()
time.sleep(1)
robot.StopMotion()
time.sleep(1)
robot.CloseRPC()
