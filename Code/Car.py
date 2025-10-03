from fairino import Robot

robot = Robot.RPC('192.168.58.2')


test_pos = [197, 556, 875, -129, 63, -80]
vel = 50
tool=1
user=0
blendR = 0

rtn = robot.MoveL(desc_pos=test_pos,tool=tool,vel=vel, user=user, blendR=blendR)
print(rtn)

robot.CloseRPC()