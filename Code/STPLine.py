from fairino import Robot
# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.58.2')
j1 = [-11.904, -99.669, 117.473, -108.616, -91.726, 74.256]
j2 = [-45.615, -106.172, 124.296, -107.151, -91.282, 74.255]
j3 = [-29.777, -84.536, 109.275, -114.075, -86.655, 74.257]
j4 = [-31.154, -95.317, 94.276, -88.079, -89.740, 74.256]
desc_pos1 = [-419.524, -13.000, 351.569, -178.118, 0.314, 3.833]
desc_pos2 = [-321.222, 185.189, 335.520, -179.030, -1.284, -29.869]
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
robot.SetSpeed(20)
rtn = robot.MoveJ(joint_pos=j1, tool=tool, user=user, vel=vel, blendT=blendT)
print(f"movej errcode: {rtn}")
rtn = robot.MoveL(desc_pos=desc_pos2, tool=tool, user=user, vel=vel, blendR=blendR)
print(f"movel errcode: {rtn}")
# rtn = robot.MoveC(desc_pos_p=desc_pos3, tool_p=tool, user_p=user, desc_pos_t=desc_pos4, tool_t=tool, user_t=user, blendR=blendR)
print(f"movec errcode: {rtn}")
rtn = robot.MoveJ(joint_pos=j2, tool=tool, user=user, vel=vel, blendT=blendT)
print(f"movej errcode: {rtn}")
rtn = robot.Circle(desc_pos_p=desc_pos3, tool_p=tool, user_p=user, desc_pos_t=desc_pos1, tool_t=tool, user_t=user)
print(f"circle errcode: {rtn}")
rtn = robot.MoveCart(desc_pos=desc_pos4, tool=tool, user=user, blendT=blendT)
print(f"MoveCart errcode: {rtn}")
robot.CloseRPC()