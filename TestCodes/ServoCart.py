import time

import calc
from fairino import Robot

# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.178.23')
desc_pos_dt = [0.3, 0.9, 0, 0, 0, 0]  # [x, y, z, rx, ry, rz] grote van de stap??
# desc_pos_dt[2] = -0.5
pos_gain = [1, 1, -0, 0.0, 0.0, 0.0]  # De hoeveel heid van die stap
temp_pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
movement = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
mode = 2
vel = 1.0
acc = 1.0
cmdT = 0.008
filterT = 0.0
gain = 0.0
flag = 0
count = 10
robot.SetSpeed(10)
a = 0


def move():
    global count, movement, temp_pos, pos_gain

    pos_gain[0] += 0.1
    time.sleep(0.01)
    rtn, pos = robot.GetActualTCPPose()
    print(robot.GetActualTCPPose())
    r = calc.getR(pos[0], pos[1])

    print(a)

    r += 1
    temp_pos[0], temp_pos[1] = calc.increaseR(r, a)
    movement[0] = temp_pos[0] - pos[0]
    movement[1] = temp_pos[1] - pos[1]
    # movement = temp_pos - pos
    print(movement)
    time.sleep(0.01)
    rtn = robot.ServoCart(mode=mode, desc_pos=desc_pos_dt, pos_gain=movement, acc=acc, vel=vel, cmdT=cmdT,
                          filterT=filterT, gain=gain)
    print(rtn)
    print(robot.GetMotionQueueLength())
    if rtn == 14:
        robot.ResetAllError()
    count -= 1
    time.sleep(cmdT)


rtn, pos = robot.GetActualTCPPose()
a = calc.getA(pos[0], pos[1])
while count > 0:
    move()

robot.CloseRPC()
