Historie
--------

Die Historie zeichnet sämtliche Änderungen (hinzufügen, bearbeiten, löschen) an den folgenden Models des Systems auf:

* django.contrib.auth.models.User (Systemnutzer)
* aemter.* (alle Models der App aemter)
* mitglieder.* (alle Models der App mitglieder)

Diese Einträge können von Administratoren des Systems auf der entsprechenden Seite unter ./admin/historie eingesehen werden.

Abhängigkeiten
~~~~~~~~~~~~~~

django-simple-history
"""""""""""""""""""""

* Installation: ``pip install django-simple-history``
* Dokumentation: `https://django-simple-history.readthedocs.io/en/latest/ <https://django-simple-history.readthedocs.io/en/latest/>`_

django-simple-history ermöglicht das automatische Aufzeichnen des Zustands eines Models beim Ausführen einer Änderungsoperation (hinzufügen, bearbeiten, löschen).

Views
~~~~~

.. automodule:: historie.views
    :members:
    :undoc-members:

Templates
~~~~~~~~~

Alle Templates sind unter `historie/templates/historie` zu finden.

list.html
"""""""""

Enthält den Grundaufbau der Historie. Die Historie wird hier in die 3 Tabs "Mitglieder", "Ämter" und "Nutzer" unterteilt.

tabs/*
""""""

Unterteilt die drei Tabs "Mitglieder", "Ämter" und "Nutzer" ggf. in weitere Tabs, z.B. bei Mitglieder in "Stammdaten", "E-Mail-Adressen" und "Ämter".
Für jedes Model wird für jeden Historien-Eintrag im entsprechenden (Unter-)Tab eine neue Listenzeile samt Modal generiert.

tabs/_pagination.html
"""""""""""""""""""""

Enthält das Template für die Pagination (die Unterteilung der Historien-Einträge in Seiten).

row.html
""""""""

| Je nachdem, zu welchem Model der Eintrag gehört, werden hier die zum Eintrag gehörenden zusätzlichen Daten inkludiert.

| `Beispiel:` Im Model MitgliedMails werden nur die IDs der Mitglieder gespeichert. Damit die Historie aber lesbarer und einfacher verständlich ist,
    werden z.B. Vor- und Nachname des zugehörigen Mitglieds ermittelt, einmal zum aktuellen und einmal zum Zeitpunkt der Erstellung des Historien-Eintrags.

| Falls der Historien-Eintrag zur Änderung eines Datensatzes gehört, werden außerdem die zusätzlichen Daten zum Vorher-Datensatz inkludiert.

rowContent.html
"""""""""""""""

Der eigentliche Inhalt eines Datensatzes. Hier wird der Grundaufbau der Zeile in der angezeigten Liste von Einträgen sowie des zugehörigen Modals beschrieben.

_titleBuilder.html
""""""""""""""""""

Beschreibt, wie der Titel, welcher in der Liste von Einträgen sowie auf dem Modal angezeigt wird, zusammengebaut wird.

_noResultsRow.html
""""""""""""""""""

Wird inkludiert, falls zu einer Suchanfrage bzw. zu einem Model keine Historien-Einträge vorhanden sind.

_modalDataIncludes.html
"""""""""""""""""""""""

Je nachdem, zu welchem Model der Eintrag gehört, wird hier der entsprechende Inhalt des zugehörigen Modals inkludiert.

modalData/*
"""""""""""

Für jedes Model wird hier beschrieben, welche Daten wie im zugehörigen Modal präsentiert werden sollen. Falls der Historien-Eintrag zur Änderung eines bestehenden Datensatzes
gehört, wird ebenfalls der Datensatz vor der Änderung mitsamt zusätzlichen Daten angezeigt.


Template Tags
~~~~~~~~~~~~~

.. automodule:: historie.templatetags.t_historie.to_class_name
    :members:
    :undoc-members:

.. automodule:: historie.templatetags.t_historie.get_associated_data
    :members:
    :undoc-members: