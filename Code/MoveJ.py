from fairino import Robot
import time

robot = Robot.RPC('192.168.58.2')
robot.ActGripper(2,0)
time.sleep(1)
robot.ActGripper(2, 1)
time.sleep(1)

joint_pos = [
    [9.724, -141.33, -101.05, -27.301, 90.259, -122.14], # pick up point
    [-87.29, -110.09, -126.18, -33.232, 91.852, -137.205],    # Drop point
    [9.724, -112.39, -94.249, -63.036, 90, -122.14],   # +30 cm above pick up point
    [-87.29,-86.502, -101.31,-81.686,91.851,-137.205] # +30 cm above drop point
]


# basic setup
vel = acc = ovl = 100
tool = user = 0
blendT = -1.0
robot.SetSpeed(100)

# Open gripper
robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)

# Move to 30cm above the pickup point
robot.MoveJ(joint_pos=joint_pos[2], tool=tool, blendT=blendT, vel=vel, user=user)

# Move to pickup point and close gripper
rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, blendT=blendT, vel=vel, user=user)
print(rtn)
robot.MoveGripper(2, 78, 100, 8, 10000, 0, 0, 0, 0, 0)

# Return to 30cm above the pickup point
rtn = robot.MoveJ(joint_pos=joint_pos[2], tool=tool, blendT=blendT, vel=vel, user=user)
print(rtn)

# Move to 30cm above drop point
rtn = robot.MoveJ(joint_pos=joint_pos[3], tool=tool, blendT=blendT, vel=vel, user=user)
print(rtn)

# Move to drop point and open gripper
rtn = robot.MoveJ(joint_pos=joint_pos[1], tool=tool, blendT=blendT, vel=vel, user=user)
print(rtn)
rtn = robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
print(rtn)

# Move back to 30cm above the drop point
rtn = robot.MoveJ(joint_pos=joint_pos[3], tool=tool, blendT=blendT, vel=vel, user=user)


rtn = robot.MoveJ(joint_pos=joint_pos[1], tool=tool, blendT=blendT, vel=vel, user=user)
rtn = robot.MoveGripper(2, 78, 100, 8, 10000, 0, 0, 0, 0, 0)
rtn = robot.MoveJ(joint_pos=joint_pos[3], tool=tool, blendT=blendT, vel=vel, user=user)
rtn = robot.MoveJ(joint_pos=joint_pos[2], tool=tool, blendT=blendT, vel=vel, user=user)
rtn = robot.MoveJ(joint_pos=joint_pos[0], tool=tool, blendT=blendT, vel=vel, user=user)
rtn = robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
rtn = robot.MoveJ(joint_pos=joint_pos[2], tool=tool, blendT=blendT, vel=vel, user=user)
print(rtn)