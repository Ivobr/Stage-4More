import calc

# from fairino import Robot
#
# robot = Robot.RPC('192.168.178.23')
#
# rtn, pos = robot.GetActualTCPPose()
pos = [20, 20, 20, 20, 20, 20]
r = calc.getR(pos[0], pos[1])
a = calc.getA(pos[0], pos[1])
print(r, a)
