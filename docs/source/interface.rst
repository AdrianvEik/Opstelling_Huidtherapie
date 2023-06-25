
.. _interface:

Interface
=========

Het interface is opgedeeld in twee keuzes, een student meting of het
troubleshoot/instellingen menu. De student meting is de standaard
weergave van het programma. Hierin kan de gebruiker een meting starten
en de resultaten bekijken. In het troubleshoot/instellingen menu kan
de gebruiker de instellingen van de meting aanpassen en de meting
kalibreren.

Student meting
--------------

Het verloop van een student meting is eenvoudig en intuïtief. De gebruiker
kan een meting starten door op de knop "Student meting" te drukken. In het
initieel keuze scherm.

.. image:: /_images/keuze_scherm.png
    :align: center

Vervolgens wordt de meting gekalibreerd. Dit is een automatisch proces
waarbij de gemeten waarden uit de meting worden vergeleken met de
referentie file die is opgeslagen in Opstelling_huidtherapie/data. De
vergelijking wordt gedaan door te controleren of het gemidelde van de gemeten
waarden binnen een bepaalde marge +- de referentie waarde ligt. De marge is
instelbaar in de config file en via de instellingen van het
troubleshoot/instellingen scherm samen met een verscheidenheid van andere
parameters.

.. image:: /_images/studentent_parameters.png
    :align: center

Indien de kalibratie succesvol is verlopen wordt het volgende scherm getoond

.. image:: /_images/kalibratie_positief.png
    :align: center

Hierin kan de gebruiker de meting starten door op de knop "Start meting"
te drukken. De meting wordt gestart en de gebruiker kan de resultaten
bekijken. De resultaten worden, afhankelijk van de instellingen uit de config
file, getoond als een percentage of OD waarde. Dit is aanpasbaar via de
volgende instellingen in het troubleshoot/instellingen scherm.

.. image:: /_images/type_student_meting.png
    :align: center

Het resultaat scherm ziet er als volgt uit

.. image:: /_images/resultaat_meting.png
    :align: center

Indien de kalibratie niet succesvol is verlopen wordt het volgende scherm
getoond

.. image:: /_images/kalibratie_negatief.png
    :align: center

hierin kan worden gekozen toch door te gaan of opnieuw te kalibreren.

Troubleshoot/instellingen
-------------------------

Dit scherm is opgedeeld in twee delen,

1. De grafiek die real time gemeten waarden toont
2. De rechterkant van het scherm waarin de instellingen kunnen worden
   aangepast en numeriek waarden ingezien of data worden opgeslagen.

Het volledig scherm zal er zo uitzien

.. image:: /_images/troubleshoot_scherm.png
    :align: center

Ingezoomed naar de grafiek ziet het er als volgt uit

.. image:: /_images/grafiek_instellingen.png
    :align: center

De x en de y as kunnen worden aangepast in de instellingen waarbij voor de x-as
de volgende opties zijn:

- Tijd
- Aantal metingen

.. image:: /_images/xas_instellingen.png
    :align: center

En voor de y-as de volgende opties zijn:

- Voltage
- Intensiteit
- Transmissie
- OD-waarde

.. image:: /_images/yas_instellingen.png
    :align: center

Daarnaast kan de gebruiker de verversingstijd van de grafiek aanpassen en de
de meettijd veranderen

.. image:: /_images/vervesingstijd.png
    :align: center

of het aantal metingen dat wordt getoond in de grafiek.

.. image:: /_images/hoeveelheidmetingen.png
    :align: center

Ook is het mogelijk om in plaats van een gefixeerd aantal
datapunten te meten iedere meting toe te voegen aan de grafiek. Dit kan
worden ingesteld door het meettype te veranderen van "N-samples" naar "Live
Data additie".

.. image:: /_images/meettype_instelling.png
    :align: center

Verder wordt aan de rechterkant van het scherm de data uit de meest recente
meting, die ook geplot is, getoond zoals het gemiddelde +- standaard deviatie

.. image:: /_images/real_time_ingelezen_data.png
    :align: center

en hieronder wordt het resultaat van de laatst uitgevoerde student meting
getoond.

.. image:: /_images/laatste_student_meting.png
    :align: center

Ook is het mogelijk om de data uit de laatste meting op te slaan in een
.txt bestand. Dit kan door op de knop "Save data" te drukken.

.. image:: /_images/save_data.png
    :align: center

Of de assen/waarden te resetten door op de knop "Reset" te drukken. De meting
kan worden gestopt door op de knop "Stop meting" te drukken of gestart via
de "start" knop.

.. image:: /_images/reset_stop_start.png
    :align: center

Er bevindt zich ook een link naar de student meting in het troubleshoot/
instellingen scherm. Deze link is te vinden onder de knop "Student meting".
