
.. _quickstart:

Quickstart
==========

In vogelvlucht wordt hier een overzicht gegeven van de belangerijkste functies
en mogelijkheden van de module. Voor meer informatie over de functies en
mogelijkheden wordt verwezen naar de documentatie van de module.

Installeren van de module gaat via github. De module is te vinden op
https://github.com/AdrianvEik/Opstelling_Huidtherapie

en kan geinstalleerd worden met het commando:

.. code-block:: bash

    pip install git+https://github.com/AdrianvEik/Opstelling_Huidtherapie

De module kan vervolgens geimporteerd worden met:

.. code-block:: python

    import Opstelling_Huidtherapie as oh

om het hoofdscherm op te starten kan deze worden aangeroepen worden via
de Base_interface klasse:

.. code-block:: python

    oh.Base_interface()

wat direct het keuze scherm tussen de verschillende onderdelen van de module opent.

.. image:: /_images/keuze_scherm.png
    :align: center

De verschillende onderdelen van de module zijn:

* :ref:`Physics Interface <physics_interface>`
* :ref:`Student Measurement interface <Student_Measurement_interface>`