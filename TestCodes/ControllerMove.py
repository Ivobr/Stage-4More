#*
# Testing the blendT function to get a smooth movement while sending just cords
# *#

from fairino import Robot
import time

robot = Robot.RPC('192.168.178.23')
blendT=500.0
sleep = 0.0

start_point = [[625, -600.945, -0.246, -179, -0.404, 41.868],
               [625, 334.438, -0.246, -179, -0.404, 41.868],
               [225, 534.438, -0.246, -179, -0.404, 41.868]]

rtn = robot.MoveCart(desc_pos=start_point[0], tool=0, user=0, vel=50, blendT=blendT)
print(rtn)
# time.sleep(sleep)
# rtn = robot.MoveCart(desc_pos=start_point[1], tool=0, user=0, vel=75, blendT=blendT)
# print(rtn)
# time.sleep(sleep)
# rtn = robot.MoveCart(desc_pos=start_point[2], tool=0, user=0, vel=100, blendT=blendT)
# print(rtn)
#
#
# rtn = robot.MoveCart(desc_pos=start_point[2], tool=0, user=0, vel=50, blendT=blendT)
# print(rtn)
# time.sleep(sleep)
# rtn = robot.MoveCart(desc_pos=start_point[1], tool=0, user=0, vel=75, blendT=blendT)
# print(rtn)
# time.sleep(sleep)
# rtn = robot.MoveCart(desc_pos=start_point[0], tool=0, user=0, vel=100, blendT=blendT)
# print(rtn)
i = 0
time.sleep(5)

# niet telkens een nieuw pos opvragen maar op eentje doorrekenen
rtn, pos = robot.GetActualTCPPose()
vel = 50

#simuleert controller joystick input
while i < 10:
    print("Nu start")


    #als vel berekent wordt kan deze elke keer meegegeven worden maybe
    pos[1] += 100
    rtn = robot.MoveCart(desc_pos=pos, tool=0, user=0, vel=vel, blendT=blendT)
    print(rtn)
    time.sleep(sleep)
    i += 1
    # if vel > 100:
    #   vel += 5
    print("i = ", i)
robot.ResetAllError()