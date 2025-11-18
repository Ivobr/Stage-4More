import time

from fairino import Robot

# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.178.23')
desc_pos_dt = [0.5, 0.5, 1, 0, 0, 0]  # [x, y, z, rx, ry, rz] grote van de stap??
# desc_pos_dt[2] = -0.5
pos_gain = [0.0, 0.0, -1, 0.0, 0.0, 0.0]  # De hoeveel heid van die stap
mode = 2
vel = 0.0
acc = 0.0
cmdT = 0.008
filterT = 0.0
gain = 0.0
flag = 0
count = 100
robot.SetSpeed(20)
while count > 0:
    time.sleep(0.001)
    rtn = robot.ServoCart(mode=mode, desc_pos=desc_pos_dt, pos_gain=pos_gain, acc=acc, vel=vel, cmdT=cmdT,
                          filterT=filterT,
                          gain=gain)
    print(rtn)
    count -= 1
    time.sleep(cmdT)
robot.CloseRPC()
