from fairino import Robot
import time
robot = Robot.RPC('192.168.58.2')
#*
# Aansluiting:
# +24V -> + LED - -> DO0
# 0V -> Button -> DI1
# Niet aansluiten op DI0 als er al een led op DO0 zit
print("LETS GET READY TO RUMBLE")


while True:
    rtn, state = robot.GetDI(1)
    print(rtn)
    if state:
        rtn = robot.SetDO(0,1)
    else:
        rtn = robot.SetDO(0,0)
    time.sleep(1)
