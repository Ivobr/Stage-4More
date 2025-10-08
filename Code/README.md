# Function deep dives

Kleine uitleg van de functie van elke functie welke ik tot nu toe heb gebruikt.\
Met uitleg van de parameters.

## Gripper
Hier alle functies welke worden gebruikt voor het gebruiken van de gripper.\
**KIJK OP WELKE INDEX DE GRIPPER ZIT VIA DE WEBAPP**

### ``MoveGripper(Index, Pos, vel, force, max_time, block, type, rotNum, rotVel, rotTorque)``
    -**Check index via webapp**
    - index = int aansluitingspunt
    - pos = int positie (0 = open, 100 = dicht)
    - vel = snelheid in procent
    - force = kracht in procent
    - maxtime = De maximale tijd voor een timeout error in ms


## Movement
Hier alle functies welke worden gebruikt voor het verplaatsen van de arm.

### ``DragTeachSwitch(State)``
    Zet robot in drag mode. Hierdoor kan de robot vrij worden bewogen met de hand\
    - State = 0 OR 1
        - 0 zet dragmode uit
        - 1 zet dragmode aan

### ``GetActualJointPosDegree()``
    - Geef niks mee
    - return (error, [pos]):
        - error code = 0 is goed rest niet
        - [pos] = array van graden. De waardes van de hoeken van de servo motors.
### ``MoveJ(Joint_pos, tool, user, vel, blendT)``
    - Joint_pos = array met de waardes van hoe de hoeken moeten zijn
    - Tool = 0
    - user = 0
    - vel = percentage van snelheid arm (wordt gecapt door de webapp dus als de webapp wordt gecapt op 30% en je kiest ``vel = 10`` wordt er op 3% snelheid gedraaid)
    - blendT = 0
### ``MoveCart(desc_pos, tool, user, blendT)``
    - desc_pos = array met xyz waarden en de rotatie - [x,y,z,rx,ry,rz]
    
### ``robot.ServoJ(joint_pos, axisPos, cmdT, filterT, gain)``
    Voor snelle preciese bewegingen van de servo motoren zelf
    In 1 keer bewegen via MoveJ is sneller
