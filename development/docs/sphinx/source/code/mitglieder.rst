Mitglieder
----------

Die Django-Applikation "mitglieder" dient zur Verwaltung (Anzeigen, Erstellen, Löschen, Bearbeiten) von Mitgliedern des StuRas. Nutzer, bei denen es sich nicht um Admins handelt, sind dabei nur zum Einsehen der Mitgliederdaten befugt.

Zu jedem Mitglied werden folgende Attribute gespeichert:

* Vorname
* Nachname
* Spitzname (optional)
* Ämter (optional)
* E-Mail-Adresse(n) (optional)
* Anschrift (optional)
* Telefonnummer(n) (optional)

Abhängigkeiten
~~~~~~~~~~~~~~

simplejson
""""""""""

* Installation: ``pip install simplejson``
* Dokumentation: `https://simplejson.readthedocs.io/en/latest/ <https://simplejson.readthedocs.io/en/latest/>`_

simplejson ist ein En- und Decoder für JSON.

Views
~~~~~

.. automodule:: mitglieder.views
    :members:
    :undoc-members:

Templates
~~~~~~~~~

Alle Templates sind unter `mitglieder/templates/mitglieder` zu finden.

aemter.html
"""""""""""

Enthält die Felder für den Kandidaturzeitraum und Dropdowns für Attribute eines Amts. Initial wird neben den Textfeldern nur das Dropwdown für ein Referat angezeigt. Die restlichen Dropdowns werden über die Auswahl eines Referats bzw. Bereichs angezeigt.


amt_dropdown_list_options.html
""""""""""""""""""""""""""""""

Dropdown zur Auswahl eines Amts. Die angezeigten Auswahlmöglichkeiten hängen vom gewählten Bereich ab.


bereich_dropdown_list_options.html
""""""""""""""""""""""""""""""""""

Dropdown zur Auswahl eines Bereichs. Die angezeigten Auswahlmöglichkeiten hängen vom gewählten Referat ab.

email.html
""""""""""

Enthält ein Textfeld zur Eingabe einer E-Mail-Adresse sowie einen Löschbutton zum Entfernen der jeweiligen E-Mail-Adresse.

email_input.html
""""""""""""""""

Enthält 0 bis n Kopien von `email.html` sowie einen Button, um genau eine weitere Kopie hinzuzufügen.

mitglieder.html
"""""""""""""""

Ansicht mit allen Mitgliedern, welche über eine Tabelle angezeigt werden. Über das Anklicken einer Zeile wird ein Modal mit allen Daten eines Mitglieds angezeigt.
Auch die Suche nach Mitgliedsnamen, das Löschen von Mitgliedern und das Wechseln zur `mitgliedErstellenView` kann hier durchgeführt werden.

mitglied_erstellen_bearbeiten.html
""""""""""""""""""""""""""""""""""

Ermöglicht die Eingabe aller Attribute eines bereits existierenden oder neuen Mitglieds. 

modal.html
""""""""""

Ein Modal, das alle Attribute eines Mitglieds mit einer bestimmten Id anzeigt.

row.html
""""""""

Eine Tabellenzeile, um Name, Vorname, Ämter, E-Mail-Adressen und die Telefonnummer eines Mitglieds anzuzeigen. Admins wird hier zusätzlich eine Checkbox und ein Button zum Bearbeiten des Mitglieds angezeigt.
Wird von `mitglieder.html` inkludiert.