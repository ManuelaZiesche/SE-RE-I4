Checklisten
-----------

Checklisten allow administrators to keep track of which tasks need to be completed in order to welcome a new member (Mitglied) to StuRa or a new Funktion inside of the StuRa.
A Checkliste may consist of a set of general tasks (Aufgaben) and/or, if a Funktion was selected, all permissions (Rechte) that have to be granted to the member (Mitglied).

Models
~~~~~~

.. automodule:: checklisten.models
    :members:
    :undoc-members:

Views
~~~~~

.. automodule:: checklisten.views
    :members:
    :undoc-members:

Templates
~~~~~~~~~

All templates can be found under ``checklisten/templates/checklisten``.

main_screen.html
""""""""""""""""

This template contains the main page of the app. Each Checkliste is represented by a card and consists of three main elements:

* The header contains the name of the Mitglied and, if specified, the Funktion that the Checkliste was created for.
* The general tasks section only exists if specified while creating the Checkliste and displays all ChecklisteAufgabe objects associated with the Checkliste.
* The permissions section only exists if a Funktion was selected for this Checkliste and displays all CheckllisteRecht objects associated with the Checkliste.

Tasks can only be checked if the user is administrator; otherwise, the checkboxes are disabled. The same goes for creating a new Checkliste; otherwise, the create button is not visible.
The template also contains JavaScript methods used to make AJAX requests to the server, e.g. to complete task or delete a Checkliste. Refer to the source code comments for more information.

_createModal.html
"""""""""""""""""

This template contains the modal that is shown when creating a new Checkliste. The modal includes:

* A dropdown to select the Mitglied that the Checkliste shall be created for. Please not that only the latest 20 Mitglieder are shown to improve performance.
* A dropdown to select the Funktion that the Checkliste shall be created for. It only contains Funktionen belonging to the Mitglied selected beforehand.
* A checkbox to determine whether the set of general tasks (Aufgaben) shall be included in the Checkliste. Will be force-checked and disabled if no Funktion is selected to prevent empty checklists from being created.

The template also contains JavaScript methods to populate the Funktionen dropdown via an AJAX request to the server, as well as to correctly disable and check the general tasks checkbox if no Funktion was selected. Refer to the source code comments for more information.

_deleteModal.html
"""""""""""""""""

This template only contains a confirmation modal if the user is trying to delete a Checkliste to prevent accidental deletions.

_funktionSelectOptions.html
"""""""""""""""""""""""""""

This template is used to generate the Funktion dropdown options for the create modal. It is only used by the ``get_funktionen`` view and is not referenced directly in other templates.

Template Tags
~~~~~~~~~~~~~

.. automodule:: checklisten.templatetags.t_checklisten.get_perms
    :members:
    :undoc-members:

.. automodule:: checklisten.templatetags.t_checklisten.get_tasks
    :members:
    :undoc-members:

