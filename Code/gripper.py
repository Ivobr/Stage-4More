from fairino import Robot
import time

# Connect to robot
robot = Robot.RPC('192.168.58.2')

try:
    print("=== Sequential Gripper Movements ===")
    
    
    robot.ActGripper(2,0)
    time.sleep(3)
    robot.ActGripper(2, 1)
    time.sleep(3)
    
    # Movement sequence with proper waiting
    movements = [
        (35.0, "Partially open"),
        (15.0, "Partially closed"), 
        (5.0, "Mostly closed"),
        (0.0, "Fully open")
    ]
    rtn = robot.GetGripperCurPosition()
    rtn = robot.MoveGripper(2,0,100,8,10000,0,0,0,0,0)
    print("cur pos", rtn)
    rtn = robot.MoveGripper(2,78,100,8,10000,0,0,0,0,0)

    # rtn = robot.MoveGripper(2,100,100,8,10000,0,0,0,0,0)
    print("move to 100:",rtn)
    time.sleep(1)
    rtn = robot.GetGripperCurPosition()
    print("cur pos", rtn)
finally:
    robot.CloseRPC()