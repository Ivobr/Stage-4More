# Function explaining

## Move

``(Type, Cords)``

``Type``: Wat voor aansturing: onnauwkeurig (Joint_point) of Precies (Cart_point)\
``Cords``: De array met de punten voor het bewegen\


Voor cartpos maybe [``GetActualToolFlangePose(flag=1)``](https://fairino-doc-en.readthedocs.io/latest/SDKManual/PythonRobotStatusInquiry.html#get-the-current-end-flange-position)
of [``GetActualTCPPose(flag=1)``](https://fairino-doc-en.readthedocs.io/latest/SDKManual/PythonRobotStatusInquiry.html#get-current-tool-position)

## Grijper aansturen

Boolean met open of dicht

## Input handling

Kan een thread worden welke de sensor uitleest en de main aan wakkert als de sensor waarde hoog wordt.