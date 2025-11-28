from fairino import Robot
import time

robot = Robot.RPC('192.168.178.23')
plimit = [170.0, 80.0, 150.0, 80.0, 170.0, 160.0]
robot.SetLimitPositive(plimit)
nlimit = [-170.0, -260.0, -150.0, -260.0, -170.0, -160.0]
robot.SetLimitNegative(nlimit)
error, neg_deg = robot.GetJointSoftLimitDeg(0)
print(
    f"pos limit deg: {neg_deg[1]}, {neg_deg[3]}, {neg_deg[5]}, {neg_deg[7]}, {neg_deg[9]}, {neg_deg[11]}")
print(
    f"neg limit deg: {neg_deg[0]}, {neg_deg[2]}, {neg_deg[4]}, {neg_deg[6]}, {neg_deg[8]}, {neg_deg[10]}")
robot.CloseRPC()
