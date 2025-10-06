from fairino import Robot
import time
# Establish a connection with the robot controller and return a robot object if the connection is successful
robot = Robot.RPC('192.168.58.2')
joint_points = [
    [-89, -55, -0.3, -122, -92, 45],
    [-95.12, -50.63, -8.22, -52.05, -90.06, 45]# pickup

]

drop_points = [
     [-95, -50, -0.5, -51.6, -90, -45],    # drop point 2
    [-89.35, -50.14, -0.42, -51.80, -90.92, -44.99], # drop point 3
    [-100, -48, -9.7, -48, -97, -56]    # drop point 4
]

offset_pos = [0] * 6
epos = [0] * 4
tool = user = 0
vel = acc = ovl = 100.0
blendT = -1.0
flag = 0
robot.SetSpeed(20)
robot.ActGripper(2,0)


pick = True
dropped = 0
time.sleep(3)
robot.ActGripper(2, 1)
time.sleep(3)

def move(point):
    global dropped
    global pick
    if pick == True:
        rtn = robot.MoveJ(joint_pos=joint_points[0], tool=tool, user=user, vel=vel)
        print(rtn)
        print("Open gripper")

        robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
        print("Wait for closing signal")
        text = input("Press enter to close gripper")

        robot.MoveGripper(2, 78, 100, 8, 10000, 0, 0, 0, 0, 0)
        print("Gripper closed")
        pick = False
    else:
        rtn = robot.MoveJ(joint_pos=point,tool=tool,user=user,vel=vel)
        print(rtn)
        rtn = robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
        print(rtn)
        point[1] -= 10
        rtn = robot.MoveJ(joint_pos=point, tool=tool, user=user, vel=vel)
        print(rtn)
        dropped = dropped + 1
        pick = True



move(joint_points[0])
print("Move to drop point")
move(drop_points[dropped])
print("Dropped: ", dropped)
move(joint_points[0])
move(drop_points[dropped])
print("Dropped: ", dropped)

# rtn = robot.MoveJ(joint_pos=drop_points[0], tool=tool, user=user, vel=vel)
# print(rtn)
# rtn = robot.MoveJ(joint_pos=drop_points[1], tool=tool, user=user, vel=vel)
# print(rtn)

# robot.MoveJ(joint_pos=drop_points[0],tool=tool,user=user,vel=vel)
# robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
# robot.MoveJ(joint_pos=drop_points[1],tool=tool,user=user,vel=vel)
robot.CloseRPC()


