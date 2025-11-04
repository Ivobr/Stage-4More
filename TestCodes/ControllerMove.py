#*
# Testing the blendT function to get a smooth movement while sending just cords
# *#

from fairino import Robot
import time
import calc
x = 0
y = 0
z = 0
r = 0
a = 0

robot = Robot.RPC('192.168.178.23')
blendT=500.0
sleep = 0.0

start_point = [[-625, 600.945, -0.246, -179, -0.404, 41.868],
               [625, 334.438, -0.246, -179, -0.404, 41.868],
               [225, 534.438, -0.246, -179, -0.404, 41.868]]

rtn = robot.MoveCart(desc_pos=start_point[0], tool=0, user=0, vel=50, blendT=blendT)
print(rtn)

rtn, pos = robot.GetActualTCPPose()
print(pos)
a = calc.getA(pos[0], pos[1])
r = calc.getR(pos[0], pos[1])
x = pos[0]
y = pos[1]
z = pos[2]
print(a, r)
print(calc.rIncrement(r,a))

i = 0
time.sleep(5)

# niet telkens een nieuw pos opvragen maar op eentje doorrekenen
rtn, pos = robot.GetActualTCPPose()
vel = 50

#simuleert controller joystick input
while i < 100:
    print("Nu start")


    #als vel berekent wordt kan deze elke keer meegegeven worden maybe
    pos[0] += 10
    pos[1] = calc.calcPoint(pos[0], r, 0)
    rtn = robot.MoveCart(desc_pos=pos, tool=0, user=0, vel=vel, blendT=blendT)
    print(rtn)
    time.sleep(sleep)
    i += 1
    # if vel > 100:
    #   vel += 5
    print("i = ", i)
robot.ResetAllError()