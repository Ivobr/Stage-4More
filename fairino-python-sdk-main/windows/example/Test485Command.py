from fairino import Robot
import time
# A connection is established with the robot controller. A successful connection returns a robot object
robot = Robot.RPC('192.168.58.2')


def auxservoset(self):
    """485 extension axis parameter setting"""
    error = robot.AuxServoSetParam(servoId=1,servoCompany=1,servoModel=1,servoSoftVersion=1,servoResolution=131072,axisMechTransRatio=13.45)
    print("AuxServoSetParam return ",error)
    error,servoCompany,servoModel,servoSoftVersion,servoResolution,axisMechTransRatio = robot.AuxServoGetParam(servoId=1)
    print("Servo driver company:",servoCompany,"Servo driver model:",servoModel,"servoSoftVersion:",servoSoftVersion,"Encoder resolution:",servoResolution,"Mechanical transmission ratio:",axisMechTransRatio)

def auxservoenable(self):
    """485 extension axis enable, homing, speed mode"""
    error = robot.AuxServoSetControlMode(servoId=1,mode=1)
    print("AuxServoSetControlMode return ", error)
    time.sleep(2)
    error = robot.AuxServoEnable(servoId=1, status=0)
    print("AuxServoEnable return ", error)
    time.sleep(2)
    error = robot.AuxServoEnable(servoId=1, status=1)
    print("AuxServoEnable return ", error)
    time.sleep(2)
    error = robot.AuxServoHoming(servoId=1, mode=1,searchVel=20,latchVel=20,acc=100)
    print("AuxServoHoming return ", error)
    time.sleep(2)

    error = robot.AuxServoSetTargetSpeed(servoId=1,speed=30,acc=100)
    print("AuxServoSetTargetSpeed return ", error)
    time.sleep(2)
    error = robot.AuxServoSetTargetSpeed(servoId=1, speed=-50,acc=100)
    print("AuxServoSetTargetSpeed return ", error)
    time.sleep(2)
    error = robot.AuxServoSetTargetSpeed(servoId=1, speed=0,acc=100)
    print("AuxServoSetTargetSpeed return ", error)
    time.sleep(2)

def auxservoposmodel(self):
    """485 extension axis position mode"""
    error = robot.AuxServoSetControlMode(servoId=1, mode=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=1)
    time.sleep(1)
    error = robot.AuxServoHoming(servoId=1, mode=1, searchVel=20, latchVel=20, acc=100)
    time.sleep(1)

    error = robot.AuxServoSetTargetPos(servoId=1,pos=200, speed=30,acc=100)
    print("AuxServoSetTargetPos return ", error)
    time.sleep(2)
    error = robot.AuxServoSetTargetPos(servoId=1, pos=-300, speed=30, acc=100)
    print("AuxServoSetTargetPos return ", error)
    time.sleep(2)

def auxservostate(self):
    """485 extension axis status detection"""
    error = robot.AuxServoSetControlMode(servoId=1, mode=1)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=1)
    time.sleep(1)
    error = robot.AuxServoHoming(servoId=1, mode=1, searchVel=20, latchVel=20, acc=100)
    time.sleep(1)

    error = robot.AuxServoSetTargetSpeed(servoId=1, speed=50,acc=100)
    time.sleep(2)
    error = robot.AuxServoSetTargetSpeed(servoId=1, speed=-70,acc=100)

    error = robot.AuxServosetStatusID(servoId=1)
    print("AuxServosetStatusID return ", error)

    while True:
        print("Extension axis position:",robot.robot_state_pkg.auxState.servoPos,"Extension axis speed:",robot.robot_state_pkg.auxState.servoVel)
        time.sleep(0.1)

def auxservoacc(self):
    """485 extension axis acceleration"""
    error = robot.AuxServoSetControlMode(servoId=1, mode=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=1)
    time.sleep(1)
    error = robot.AuxServoHoming(servoId=1, mode=1, searchVel=20, latchVel=20, acc=100)
    time.sleep(1)

    error = robot.AuxServoSetTargetPos(servoId=1,pos=500, speed=100,acc=80)
    print("AuxServoSetTargetPos return ", error)
    time.sleep(2)
    error = robot.AuxServoSetTargetPos(servoId=1, pos=-500, speed=100, acc=10)
    print("AuxServoSetTargetPos return ", error)
    time.sleep(2)

def auxservostop(self):
    """485 extension axis emergency stop"""
    error = robot.AuxServoSetParam(1, 1, 1, 1, 130172, 15.45)
    print("AuxServoSetParam return", error)

    error = robot.AuxServoEnable(1, 0)
    print("AuxServoEnable return", error)
    time.sleep(1)

    error = robot.AuxServoSetControlMode(1, 1)
    print("AuxServoSetControlMode return", error)
    time.sleep(1)
    error = robot.AuxServoEnable(1, 1)
    print("AuxServoEnable return", error)
    time.sleep(1)
    error = robot.AuxServoHoming(1, 1, 10, 10, 100)
    print("AuxServoHoming return", error)
    time.sleep(4)
    error = robot.AuxServoSetEmergencyStopAcc(4000, 5000)
    print("AuxServoSetEmergencyStopAcc return", error)
    time.sleep(1)
    error = robot.AuxServoGetEmergencyStopAcc()
    print("AuxServoGetEmergencyStopAcc return", error)
    time.sleep(1)

    error = robot.AuxServoSetAcc(490, 500)
    print("AuxServoSetAcc", error)
    error = robot.AuxServoSetTargetSpeed(1, 500, 100)
    print("AuxServoSetTargetSpeed", error)

    error, joint = robot.GetActualJointPosDegree()
    print("GetActualJointPosDegree", error, joint)

    joint[0] = joint[0] + 20
    error = robot.MoveJ(joint, 1, 0, blendT=1)
    print("MoveJ", error)
    joint[0] = joint[0] - 90
    error = robot.MoveJ(joint, 1, 0, blendT=1)
    print("MoveJ", error)

    n = 0
    while n < 10:
        time.sleep(0.1)
        for i in range(1):
            print("auxState.servoVel:", robot.robot_state_pkg.auxState.servoVel)
            print("auxState.servoState:", robot.robot_state_pkg.auxState.servoState)
            print("auxState.servoState_emergency stop:", (robot.robot_state_pkg.auxState.servoState >> 7) & 0x01)
        if 1 == (robot.robot_state_pkg.auxState.servoState >> 7) & 0x01:
            n = n + 1

def auxservostopstate(self):
    """485 extension axis emergency stop status print"""
    error = robot.AuxServoSetParam(1, 1, 1, 1, 130172, 15.45)
    print("AuxServoSetParam return", error)

    error = robot.AuxServoEnable(1, 0)
    print("AuxServoEnable return", error)
    time.sleep(1)

    error = robot.AuxServoSetControlMode(1, 1)
    print("AuxServoSetControlMode return", error)
    time.sleep(1)
    error = robot.AuxServoEnable(1, 1)
    print("AuxServoEnable return", error)
    time.sleep(1)
    error = robot.AuxServoHoming(1, 1, 10, 10, 100)
    print("AuxServoHoming return", error)
    time.sleep(4)
    error = robot.AuxServoSetEmergencyStopAcc(40, 50)
    print("AuxServoSetEmergencyStopAcc return", error)
    time.sleep(1)
    error = robot.AuxServoGetEmergencyStopAcc()
    print("AuxServoGetEmergencyStopAcc return", error)
    time.sleep(1)

    error = robot.AuxServoSetAcc(490, 500)
    print("AuxServoSetAcc", error)
    error = robot.AuxServoSetTargetSpeed(1, 500, 100)
    print("AuxServoSetTargetSpeed", error)

    error, joint = robot.GetActualJointPosDegree()
    print("GetActualJointPosDegree", error, joint)

    joint[0] = joint[0] + 20
    error = robot.MoveJ(joint, 1, 0, blendT=1)
    print("MoveJ", error)
    joint[0] = joint[0] - 90
    error = robot.MoveJ(joint, 1, 0, blendT=1)
    print("MoveJ", error)

    n = 0
    while n < 10:
        time.sleep(0.1)
        for i in range(1):
            print("auxState.servoVel:", robot.robot_state_pkg.auxState.servoVel)
            print("auxState.servoState:", robot.robot_state_pkg.auxState.servoState)
            print("auxState.servoState_emergency stop:", (robot.robot_state_pkg.auxState.servoState >> 7) & 0x01)
        if 1 == (robot.robot_state_pkg.auxState.servoState >> 7) & 0x01:
            n = n + 1

    time.sleep(4)
    error = robot.ResetAllError()
    print("ResetAllError",error)
    time.sleep(4)

    n=0
    while n<10:
        time.sleep(0.1)
        for i in range(1):
            print("auxState.servoVel:", robot.robot_state_pkg.auxState.servoVel)
            print("auxState.servoState:", robot.robot_state_pkg.auxState.servoState )
            print("auxState.servoState_emergency stop:", (robot.robot_state_pkg.auxState.servoState >> 7)& 0x01)
        if 1==(robot.robot_state_pkg.auxState.servoState >> 7)& 0x01:
            n=n+1

def auxservovelacc(self):
    """485 extension axis speed mode acceleration"""
    error = robot.AuxServoSetControlMode(servoId=1, mode=1)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=1)
    time.sleep(1)
    error = robot.AuxServoHoming(servoId=1, mode=1, searchVel=20, latchVel=20, acc=100)
    time.sleep(2)

    error = robot.AuxServoSetTargetSpeed(servoId=1, speed=200, acc=100)
    print("AuxServoSetTargetSpeed return ", error)
    time.sleep(4)
    error = robot.AuxServoSetTargetSpeed(servoId=1, speed=-200, acc=20)
    print("AuxServoSetTargetSpeed return ", error)
    time.sleep(4)
    error = robot.AuxServoSetTargetSpeed(servoId=1, speed=0, acc=20)
    print("AuxServoSetTargetSpeed return ", error)
    time.sleep(2)

def auxservoposacc(self):
    """485 extension axis position mode acceleration"""
    error = robot.AuxServoSetControlMode(servoId=1, mode=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=1)
    time.sleep(1)
    error = robot.AuxServoHoming(servoId=1, mode=1, searchVel=20, latchVel=20, acc=100)
    time.sleep(2)

    error = robot.AuxServoSetTargetPos(servoId=1, pos=300, speed=200, acc=100)
    print("AuxServoSetTargetPos return ", error)
    time.sleep(4)
    error = robot.AuxServoSetTargetPos(servoId=1, pos=-300, speed=200, acc=10)
    print("AuxServoSetTargetPos return ", error)
    time.sleep(4)

def auxservoaccchange(self):
    """485 extension axis change acceleration"""
    error = robot.AuxServoSetControlMode(servoId=1, mode=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=0)
    time.sleep(1)
    error = robot.AuxServoEnable(servoId=1, status=1)
    time.sleep(1)
    error = robot.AuxServoHoming(servoId=1, mode=1, searchVel=20, latchVel=20, acc=100)
    time.sleep(2)
    i = 20
    while i<50:
        error = robot.AuxServoSetTargetPos(servoId=1,pos=500, speed=300,acc=0+i)
        print("AuxServoSetTargetPos return ", error)
        time.sleep(4)
        error = robot.AuxServoSetTargetPos(servoId=1, pos=-500, speed=300, acc=0+i+i)
        print("AuxServoSetTargetPos return ", error)
        time.sleep(4)
        i += 20

# auxservoset(robot)
# auxservoenable(robot)
# auxservoposmodel(robot)
# auxservostate(robot)
# auxservoacc(robot)
# auxservostop(robot)
# auxservostopstate(robot)
# auxservovelacc(robot)
# auxservoposacc(robot)
# auxservoaccchange(robot)