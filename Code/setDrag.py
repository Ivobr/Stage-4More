import time

from fairino import Robot

robot = Robot.RPC('192.168.178.23')
robot.DragTeachSwitch(1)
try:
    while True:
        print("New posistion")
        print(robot.GetActualJointPosDegree())
        print(robot.GetActualTCPPose())
        time.sleep(1)
except KeyboardInterrupt:
    robot.DragTeachSwitch(0)
    robot.CloseRPC()
