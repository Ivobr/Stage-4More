from fairino import Robot
import time
drop_pos = [-95, -49.52, -6.10, -38.36, -90.93, -135]
rest_pos=[102, -130, 13, -237, -92, -135]
kys_pos = [-94,-55,8,-71,-90,135]
kys_2pos = [-94,-55,6.75,-71,-90,135]
vel = 100
tool = 0
user = 0
blendT = 0.0


robot = Robot.RPC('192.168.58.2')

print("final")
print(robot.GetActualJointPosDegree())

rtn = robot.MoveJ(joint_pos=drop_pos, tool=tool, user=user, vel=vel, blendT=blendT)
print(f"movej error code: {rtn}")

time.sleep(2)
rtn = robot.MoveGripper(2, 100.0, 100, 8, 10000, 0, 0, 0, 0, 0)
time.sleep(5)

rtn = robot.MoveJ(joint_pos=rest_pos, tool=tool, user=user, vel=vel, blendT=blendT)
print(rtn)

time.sleep(1)
rtn = robot.MoveJ(joint_pos=drop_pos, tool=tool, user=user, vel=vel, blendT=blendT)
rtn = robot.MoveGripper(2, 0.0, 50, 8, 10000, 0, 0, 0, 0, 0)
print(f"movej error code: {rtn}")

robot.CloseRPC()