from fairino import Robot
import time

robot = Robot.RPC('192.168.178.23')
robot.DragTeachSwitch(1)
try:
    while True:
        print("new position")
        print(robot.GetActualJointPosDegree())
        print(robot.GetActualTCPPose())
        pos = robot.GetActualTCPPose()
        time.sleep(1)
except KeyboardInterrupt:
    robot.DragTeachSwitch(0)
    robot.CloseRPC()