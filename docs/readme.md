# Project medische technologie
De uitgebreide documentatie is te vinden op: \
https://opstelling-huidtherapie.readthedocs.io/en/latest/

## Introductie tot de software

Deze software is geschreven voor een project in de minor "Medische technologie"
van de Haagse Hogeschool. Hierbij is de opdracht een interface en hardware te 
ontwikkelen
dat wordt gebruikt bij een practicum voor de opleiding Huidtherapie.

## UV-Licht practicum
Het practicum heeft als doel om met UV-licht de transmissie van zonnebrandcrème
of stof te meten met een UV-LED en sensor. De sensor wordt aangestuurd vanuit
een rapsberry pi, de code in deze repo voor aansturing staat in hardware.py.

## Interface
Het interface biedt twee keuzes, het meten van de transmissie van zonnebrandcrème
of stof (Student) en het uitlezen van data over de sensor voor bugfixing 
(Physics). De interface is geschreven in python met behulp van de tkinter
library. Het figuur hieronder laat het initiële scherm zien.

![alt text](https://github.com/AdrianvEik/Opstelling_Huidtherapie/blob/master/docs/source/_images/keuze_scherm.png "Keuze scherm")

## Student
Om een simpele meting te starten aan de opstelling kiest de student voor de
optie "Student". De student krijgt dan eerst een kort laad scherm te zien
met de notificatie "verificatie gestart". Dit is om de sensor te 
kalibreren/data te verifieren en vergelijken met een referentie meting 
(aanpasbaar in de Physics instellingen). Als het verificatie proces 
negatief doorlopen is is er iets mis met de sensor/LED of er staat een sample
in de weg o.i.d. Er wordt een notificatie gegeven en kan de student simpele 
troubleshooting uitvoeren zoals ervoor zorgen dat er niks in het optische pad
staat. Het scherm laat de volgende notificatie zien:

![alt text](https://github.com/AdrianvEik/Opstelling_Huidtherapie/blob/master/docs/source/_images/kalibratie_negatief.png "Kalibratie negatief")

In het geval dat de simpele troubleshooting kan de opstelling opnieuw 
worden geverifieerd door op de knop "Opnieuw starten" te drukken. Of in het 
geval dat de opstelling visueel in orde is kan de student op de knop "Toch 
meten?" drukken. In het geval dat de opstelling wel goed is geverifieerd
is er een enkele knop op het scherm te zien die moet worden ingedrukt om 
een meting te starten:

![alt text](https://github.com/AdrianvEik/Opstelling_Huidtherapie/blob/master/docs/source/_images/kalibratie_positief.png "Kalibratie positief")

Vervolgens wordt er weer een laadbalk getoond tijdens de meting en 
vervolgens wordt het resultaat getoond:

![alt text](https://github.com/AdrianvEik/Opstelling_Huidtherapie/blob/master/docs/source/_images/resultaat_meting.png "Resultaat meting")

De student kan vervolgens op de knop "Opnieuw meten" drukken om een nieuwe
meting te starten. 

## Physics
De Physics optie is bedoeld voor het uitlezen van de sensor en LED. Dit is
bedoeld voor bugfixing en het testen van de opstelling. De interface is verder
toechelicht op readthedocs waarbij ook code-technisch wordt uitgelegd hoe de
interface werkt. De interface is te vinden op: \
https://opstelling-huidtherapie.readthedocs.io/en/latest/interface.html

