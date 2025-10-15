## Move

``MoveJ(joint_pos, tool, user, vel)``

``Cords``: De array met de punten voor het bewegen\
Verplaatst de arm doormiddel van meegegeven hoeken\
``Joint_pos``: Array[J1, J2, J3, J4, J5, J6] in graden. elke J[x] staat gelijk aan een as welke naar die hoek draait\
``Tool & user``: Geef voor standaard functies 0 mee\
``Vel``: Snelheid in % van de voorbepaalde `robospeed()` dus voor een robotspeed van 20 en vel = 10% zal de arm op 2% snelheid bewegen.

``MoveCart(decs_pos, tool, user, vel)``

Verplaatst de arm doormiddel van meegegeven coordianten\
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

``SetDo(id, state)``

Zet de gekozen pin op de gewenste state\
``Id``: Pin nummer op eerste rij aan pinnen\
``State``: Zet pin hoog 1 of laag 0

``GetDI(id)``

Lees de input waarde van pin uit\
``Id``: Pin nummer op tweede rij aan pinnen

## Safety

``SetAnticollision(mode, level, config)``

Zet collision detecie aan of uit\
``mode``: 0 level, 1 percentage\
``level``: array met de waarde voor elke joint om een collision aan te geven\
``config``: update configfile 0 ja 1 nee

``SetCollisionStrategy(strategy,safeTime,safeDistance,safeVel,safetyMargin)``

Selecteer een reactie wanneer er een collision is\
``strategy``: 0 - report error and pause, 1 - keep running, 2 - error stop, 3 - heavy moment mode, 4 - shock response mode, 5 - impact rebound mode\

**Niet verplicht**\
``safeTime``: safe stop time default 1000 ms\
``safeDistance``: safe stopping distance [1-150] mm, default: 100\
``safeVel``: safe stopping speed[50-250]mm/s, default: 250\
``safetyMargin``: safety margin [1-10], default: [10,10,10,10,10,10,10]