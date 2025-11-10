# TestCode

In deze map kunnen alle geteste codes gevonden worden. Deze codes zijn geschreven om de bewegingfuncties te testen.\
Maar ook voor het testen van de verschillende aanstuur mogelijkheden via de controller.\
Alle codes welke geschreven worden om een functionaliteit te testen worden in deze map gezet.

## Codes

* [MoveJ.py](MoveJ.py) deze code is gebruikt in het testplan/experimenteel onderzoek voor het kiezen van een
  bewegingsfunctie.
* [MoveCart.py](MoveCart.py) deze code is gebruikt in het testplan/experimenteel onderzoek voor het kiezen van een
  bewegingsfunctie.
* [Jog1.py](JOG1.py) de gebruikte code om de vloeiende versnellende beweging te maken via de controller.
* [Controller2.py](Controller2.py) de gebruikte code om de schokkende rotatie code te krijgen.
* [calc.py](calc.py) de gebruikte code om de nieuwe coordinaten uit te rekenen voor de [Controller2.py](Controller2.py)
  code.

## Move

Hieronder staan alle gebruikte functies binnen de Fairino Library en de benodigde parameters.

### ``MoveJ(joint_pos, tool, user, vel)``

``Cords``: De array met de punten voor het bewegen\
Verplaatst de arm doormiddel van meegegeven hoeken\
``Joint_pos``: Array[J1, J2, J3, J4, J5, J6] in graden. elke J[x] staat gelijk aan een as welke naar die hoek draait\
``Tool & user``: Geef voor standaard functies 0 mee\
``Vel``: Snelheid in % van de voorbepaalde `robospeed()` dus voor een robotspeed van 20 en vel = 10% zal de arm op 2%
snelheid bewegen.\
``blendT``: Geen verplichte parameter maar bedoeld om een vloeiende beweging te krijgen tussen meerdere punten.
Standaard voor geen gebruik: -1.0. Maximale waarde 500 (ms)

### ``MoveCart(decs_pos, tool, user, vel, blendT)``

Verplaatst de arm doormiddel van meegegeven coordianten\
``decs_pos``: Array[x, y, z, rx, ry, rz] in mm en graden. xy en z waardes zijn in mm en de rx, ry & rz zijn in graden\
``Tool & user``: Geef voor standaard functies 0 mee\
``Vel``: Snelheid in % van de voorbepaalde `robospeed()` dus voor een robotspeed van 20 en vel = 10% zal de arm op 2%
snelheid bewegen.\
``blendT``: Geen verplichte parameter maar bedoeld om een vloeiende beweging te krijgen tussen meerdere punten.
Standaard voor geen gebruik: -1.0. Maximale waarde 500 (ms)

## Grijper aansturen

### ``ActGripper(index, action)``

``index``: locatie waar grijper is aangesloten\
``action``: actie 0-reset, 1-activeer

### ``Movegripper(index,pos,vel,force,maxtime,block,type,rotNum,rotVel,rotTorque)``

``index``: locatie waar grijper is aangelosten\
``pos``: positie 0 = open, 100 = dicht\
``vel``: snelheid
``force``: kracht
``maxtime``: maximale tijd voordat er een timeout error wordt gegooid, sweet spot tot nu toe 10000\
Rest op 0 zetten

## Input handling

### ``SetDo(id, state)``

Zet de gekozen pin op de gewenste state\
``Id``: Pin nummer op eerste rij aan pinnen\
``State``: Zet pin hoog 1 of laag 0

### ``GetDI(id)``

Lees de input waarde van pin uit\
``Id``: Pin nummer op tweede rij aan pinnen

## Changelog

| Wie          | Datum      | Wijziging                     |
|--------------|------------|-------------------------------|
| Ivo Bruinsma | 25-09-2025 | Aanmaak document              |
| Ivo Bruinsma | 10-11-2025 | Introductie document aanmaken |