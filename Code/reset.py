from fairino import Robot
import time

robot = Robot.RPC('192.168.58.2')

try:
    time.sleep(2)
    rtn = robot.MoveGripper(2, 100.0, 100, 100, 10000, 0, 0, 0, 0, 0)
    print(rtn)
    
# maxtime = 10 seconds

    time.sleep(5)
    rtn = robot.MoveGripper(2, 0.0, 100, 100, 10000, 0, 0, 0, 0, 0) #max_time is in ms

    robot.ActGripper(2,0)

    print("a hamdula ", rtn)
    robot.CloseRPC()
    
finally:
    robot.CloseRPC()