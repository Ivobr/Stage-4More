# Function explaining

## Move

``MoveJ(joint_pos, tool, user, vel)``

Verplaatst de arm doormiddel van meegegeven hoeken\
``Joint_pos``: Array[J1, J2, J3, J4, J5, J6] in graden. elke J[x] staat gelijk aan een as welke naar die hoek draait\
``Tool & user``: Geef voor standaard functies 0 mee\
``Vel``: Snelheid in % van de voorbepaalde `robospeed()` dus voor een robotspeed van 20 en vel = 10% zal de arm op 2% snelheid bewegen.

``MoveCart(decs_pos, tool, user, vel)``

Verplaatst de arm doormiddel van meegegeven hoeken\
``decs_pos``: Array[x, y, z, rx, ry, rz] in mm en graden. xy en z waardes zijn in mm en de rx, ry & rz zijn in graden\
``Tool & user``: Geef voor standaard functies 0 mee\
``Vel``: Snelheid in % van de voorbepaalde `robospeed()` dus voor een robotspeed van 20 en vel = 10% zal de arm op 2% snelheid bewegen.


## Grijper aansturen

``ActGripper(index, action)``

``index``: locatie waar grijper is aangesloten\
``action``: actie 0-reset, 1-activeer

``Movegripper(index,pos,vel,force,maxtime,block,type,rotNum,rotVel,rotTorque)``

``index``: locatie waar grijper is aangelosten\
``pos``: positie 0 = open, 100 = dicht\
``vel``: snelheid
``force``: kracht
``maxtime``: maximale tijd voordat er een timeout error wordt gegooid, sweet spot tot nu toe 10000\
Rest op 0 zetten

## Input handling

Kan een thread worden welke de sensor uitleest en de main aan wakkert als de sensor waarde hoog wordt.

``SetDo(id, state)``

Zet de gekozen pin op de gewenste state\
``Id``: Pin nummer op eerste rij aan pinnen\
``State``: Zet pin hoog 1 of laag 0

``GetDI(id)``

Lees de input waarde van pin uit\
``Id``: Pin nummer op tweede rij aan pinnen