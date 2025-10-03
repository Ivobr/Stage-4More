from fairino import Robot
import time

# Connect to robot
robot = Robot.RPC('192.168.58.2')

try:
    print("=== Sequential Gripper Movements ===")
    
    # Activate gripper
    robot.ActGripper(2, 1)
    time.sleep(3)
    
    # Movement sequence with proper waiting
    movements = [
        (35.0, "Partially open"),
        (15.0, "Partially closed"), 
        (5.0, "Mostly closed"),
        (0.0, "Fully open")
    ]
    

    for pos, desc in movements:
        print(f"Moving to {pos}mm ({desc})...")
        rtn = robot.MoveGripper(2, pos, 30, 8, 1000, 0, 0, 0, 0, 0)
        print(f"Move result: {rtn}")
        
        if rtn == 0:
            print(f"✓ Movement started to {pos}mm")
            # Wait for movement to complete - estimate based on distance
            move_time = abs(pos - (movements[movements.index((pos, desc))-1][0] if movements.index((pos, desc)) > 0 else 0)) / 30 * 1000 + 1000
            wait_ms = int(move_time)
            print(f"Waiting {wait_ms}ms for movement to complete...")
            time.sleep(wait_ms / 1000)
        else:
            print(f"✗ Move failed with error {rtn}")
            break
    
    print("Movement sequence completed!")
    
finally:
    robot.CloseRPC()