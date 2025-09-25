from fairino import Robot
import time
#        x   y   z   rx   ry  rz
joint_point = [15, 20, 25, 145, 23, 25]
type = "obj"

tool = user = 0
vel = 50 # % of max-speed

# robot = Robot.RPC('192.168.58.2')

# robot.SetSpeed(20)

def input():
    print("Sensor leest hoog")


input()

def MoveTo(type, cords):
    match type:
        case "band":
            print("moving above obj")
            #robot.MoveJ(joint_pos=joint_point, tool=tool, user=user, vel=vel)

            type = "obj"
        case "obj":
            print("localize flower")
            time.sleep(1)
            print("going down to pick flower")
    print(cords)

MoveTo(type=type, cords=joint_point)