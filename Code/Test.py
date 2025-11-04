from fairino import Robot

robot = Robot.RPC('192.168.178.23')

rtn = robot.GetJointSoftLimitDeg()
print(rtn)

status = robot.GetRobotEmergencyStopState()
print(status)