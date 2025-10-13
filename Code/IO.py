from fairino import Robot
import time
robot = Robot.RPC('192.168.178.23')
# basic setup
tool = user = 0
blendT = -1.0
flag = 0

robot.ActGripper(2,0)
time.sleep(1)
robot.ActGripper(2, 1)
time.sleep(1)

cords = [
    # 375 -> -275
    [625, 4.438, -32.046, -179, -0.404, 41.868], # pickup point
    [-76.302, -472.35, 123.796, -179.11, -1.699, -40.09], # drop point
]
#*
# Aansluiting:
# +24V -> + LED - -> DO0
# 0V -> Button -> DI1
# Niet aansluiten op DI0 als er al een led op DO0 zit
print("LETS GET READY TO RUMBLE")

def IO():
    while True:
        rtn, state = robot.GetDI(1)
        print(rtn)
        if state:
            rtn = robot.SetDO(0,1)
            print(state)
            return 1
        else:
            rtn = robot.SetDO(0,0)
        time.sleep(1)

def move():
    rtn = robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
    print(rtn)
    # Calculate and move to 30cm above pickup point
    cords[0][2] += 300
    rtn = robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)
    print(rtn)

    # Calculate and move to pickup point
    cords[0][2] -= 300
    rtn = robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)
    print(rtn)

    # close gripper and move back up to 30cm above pickup
    rtn = robot.MoveGripper(2, 78, 100, 8, 10000, 0, 0, 0, 0, 0)
    print(rtn)
    cords[0][2] += 300
    rtn = robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)
    print(rtn)

    # Move to 30cm above drop point
    cords[1][2] += 300
    rtn = robot.MoveCart(desc_pos=cords[1], tool=tool, blendT=blendT, user=user)
    print(rtn)

    # Move to drop poit and open gripper
    cords[1][2] -= 300
    rtn = robot.MoveCart(desc_pos=cords[1], tool=tool, blendT=blendT, user=user)
    print(rtn)
    robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
    print(rtn)

    # Move 30cm above the drop point
    cords[1][2] += 300
    rtn = robot.MoveCart(desc_pos=cords[1], tool=tool, blendT=blendT, user=user)
    print(rtn)

    cords[1][2] -= 300
    rtn = robot.MoveCart(desc_pos=cords[1], tool=tool, blendT=blendT, user=user)
    rtn = robot.MoveGripper(2, 78, 100, 8, 10000, 0, 0, 0, 0, 0)
    cords[1][2] += 300
    rtn = robot.MoveCart(desc_pos=cords[1], tool=tool, blendT=blendT, user=user)
    rtn = robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)
    cords[0][2] -= 300
    rtn = robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)
    rtn = robot.MoveGripper(2, 0, 100, 8, 10000, 0, 0, 0, 0, 0)
    cords[0][2] += 300
    rtn = robot.MoveCart(desc_pos=cords[0], tool=tool, blendT=blendT, user=user)


def main():
    IO()
    move()


if __name__ == '__main__':
    main()
    robot.SetDO(0,0)