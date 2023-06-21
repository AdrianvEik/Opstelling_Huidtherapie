
.. _api:

API
###

Basis interface
===============

Het eerste keuzescherm bevat twee keuzes voor de gebruiker. De gebruiker kan kiezen tussen een studentenmeting of een
meting met de volledige functionaliteit. De studentenmeting is een vereenvoudigde versie van de meting met de volledige
functionaliteit.

De class met zijn methodes en attributen gebruikt voor dit scherm staan hieronder.

.. automodule:: src.Base_interface
   :members:
   :undoc-members:
   :show-inheritance:

Physics Interface
=================

Het hoofdscherm van de applicatie is de Physics Interface. Hierin kan de gebruiker de meting instellen en uitvoeren.
De inteface bestaat uit verschillende knoppen met functionaliteiten. Hieruit kunnen mogelijk 3 andere schermen worden geopend:
- Measurement Settings
- Save Measurement
- Student measurement

Ieder scherm dat kan worden geopend bevindt zich in zijn eigen file en class. Hieronder staan de
atributen en methodes van de physics intefrace.

.. automodule:: src.Physics_Interface.Physics_interface
   :members:
   :undoc-members:
   :show-inheritance:


Measurement Settings
--------------------

In dit scherm kan de gebruiker de instellingen van de meting aanpassen. De gebruiker kan de volgende instellingen aanpassen:
Voor de meting:
- Het meettype (N-metingen tegelijk of iedere meting aan de bestaande grafiek toevoegen)
- Het aantal metingen dat tegelijk wordt uitgevoerd.
Voor de grafiek:
- De grootheid op de x-as (tijd of nr van metingen)
- De grootheid op de y-as (spanning, intensiteit, transmissie of berekende OD waarden)
- De verversingsfrequentie van de grafiek (standaard 1000 ms)
- De stapsgrootte van de x-as
Een aantal algemene variabelen:
- De sigma factor voor de berekening van de standaarddeviatie die wordt weergegeven.
- Het pad naar de referentie meting voor verificatie van de opstelling en voor de berekening van OD/transmissie waarden.
Instellingen voor een studentenmeting:
- Het aantal datapunten dat wordt verzameld en opgeslagen tijdens een meting.
- De tijd van de algehele meting.
- Het getoonde resultaat van de meting, OD waarde en transmissie.
- Marge (in volt) voor de verificatie van de opstelling.

Hieronder staan de attributen en methodes van deze class.

.. automodule:: src.Physics_Interface.Physics_interface_Settings
   :members:
   :undoc-members:
   :show-inheritance:

Save Measurement
----------------
Om data punten op te slaan kan de gebruiker dit scherm openen. Hierbij worden alle datapunten
die zijn weergegeven in de grafiek naar een .txt file geschreven, dit is handig voor het maken van een
snelle meting of hiermee grafieken in andere programma's te maken. De save functie bevat twee opties
het pad naar de directory waar het wordt opgeslagen en de naam van het bestand.

.. automodule:: src.Physics_Interface.Physics_interface_DataManipulation
   :members:
   :undoc-members:
   :show-inheritance:

Student Measurement interface
=============================

Aanvankelijk wordt de opstelling geverifieerd. Dit gebeurt zodra de knop "Student" in het basis
interface wordt ingedrukt. Dit verifieering gebeurt in een aparte thread om ervoor te zorgen dat
de GUI niet bevriest. Het gemiddelde van de referentie meting wordt vergeleken met de reference file aangegeven
in de instellingen zoals laten zien hiervoor in de Measurement Settings. Als de gemiddelde waarde binnen de marge
valt wordt komt de student in het metingscherm. In de code wordt hiervoor het scherm ververst met nieuwe labels
en wordt de lopende balk verwijderd. Als de student op start meting drukt wordt de meting gestart,
en uitgevoerd in een aparte thread. Het resultaat wordt dan laten zien. De queue is gedeeld tussen de threads
om data te verzamelen en te laten zien in de grafiek. De student kan de meting stoppen door het programma te sluiten of de stop
knop in te drukken.

.. automodule:: src.Student_Interface.Student_interface
   :members:
   :undoc-members:
   :show-inheritance:
