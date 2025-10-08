from fairino import Robot
import time

robot = Robot.RPC('192.168.58.2')
j1 = [-11.904, -99.669, 117.473, -108.616, -91.726, 74.256]
j2 = [-45.615, -106.172, 124.296, -107.151, -91.282, 74.255]
j3 = [-29.777, -84.536, 109.275, -114.075, -86.655, 74.257]
j4 = [-31.154, -95.317, 94.276, -88.079, -89.740, 74.256]
desc_pos1 = [-45, 651, 706, -171, -8.53, 39.423]
desc_pos2 = [-276, 574, 708, 173, -6,94, 136]
desc_pos3 = [-487.434, 154.362, 308.576, 176.600, 0.268, -14.061]
desc_pos4 = [-443.165, 147.881, 480.951, 179.511, -0.775, -15.409]
offset_pos = [0, 0, 0, 0, 0, 0]
epos = [0, 0, 0, 0]
tool = 0
user = 0
vel = 100.0
acc = 100.0
ovl = 100.0
blendT = 0.0
blendR = 0.0
flag = 0
search = 0
# robot.SetSpeed(20)
# rtn = robot.MoveJ(joint_pos=j1, tool=tool, user=user, vel=vel, blendT=blendT)
# print(f"movej errcode: {rtn}")
# rtn = robot.MoveL(desc_pos=desc_pos2, tool=tool, user=user, vel=vel, blendR=blendR)
# print(f"movel errcode: {rtn}")
# # rtn = robot.MoveC(desc_pos_p=desc_pos3, tool_p=tool, user_p=user, desc_pos_t=desc_pos4, tool_t=tool, user_t=user, blendR=blendR)
# print(f"movec errcode: {rtn}")
# rtn = robot.MoveJ(joint_pos=j2, tool=tool, user=user, vel=vel, blendT=blendT)
# print(f"movej errcode: {rtn}")
# rtn = robot.Circle(desc_pos_p=desc_pos3, tool_p=tool, user_p=user, desc_pos_t=desc_pos1, tool_t=tool, user_t=user)
# print(f"circle errcode: {rtn}")
# rtn = robot.MoveCart(desc_pos=desc_pos1, tool=tool, user=user, blendT=blendT)
# time.sleep(1)
# rtn, pos = robot.GetActualTCPPose()
# print(pos)
# pos[2] = pos[2] + 100
# print(pos)
rtn = robot.MoveCart(desc_pos=desc_pos1, tool=tool, user=user, blendT=blendT)
print(rtn)
time.sleep(2)
rtn = robot.MoveCart(desc_pos=desc_pos2, tool=tool, user=user, blendT=blendT)
print(rtn)
rtn = robot.MoveCart(desc_pos=desc_pos3, tool=tool, user=user, blendT=blendT)
rtn = robot.MoveCart(desc_pos=desc_pos4, tool=tool, user=user, blendT=blendT)
rtn = robot.ServoJTStart()
print(rtn)
rtn = robot.ServoJ()
print(f"MoveCart errcode: {rtn}")
robot.CloseRPC()