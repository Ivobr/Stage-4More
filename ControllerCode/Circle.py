from fairino import Robot

r = Robot.RPC('192.168.178.23')

desc_pos3 = [-487.434, 154.362, 308.576, 176.600, 0.268, -14.061]
desc_pos1 = [-419.524, -13.000, 351.569, -178.118, 0.314, 3.833]
tool = 0
user = 0

print(r.GetSlaveHardVersion())
print(r.GetSoftwareVersion())
print(r.GetSDKVersion())
print(r.GetMotionQueueLength())
print(r.StopMotion())
print(r.GetMotionQueueLength())
print(r.GetSystemClock())