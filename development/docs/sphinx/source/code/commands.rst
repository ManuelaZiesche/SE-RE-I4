Commands
--------

delete_old_historie
~~~~~~~~~~~~~~~~~~~

.. automodule:: bin.management.commands.delete_old_historie
    :members:
    :undoc-members:

clean_duplicate_history
~~~~~~~~~~~~~~~~~~~~~~~

django-simple-history includes a command that can be used to remove all duplicate entries in the Historie. 
For example, an entry is created in MitgliedMail and MitgliedAmt when the associated Mitglied is changed, even though no changes
have been made to MitgliedMail and MitgliedAmt. To get rid of these entries, you can use:

``python manage.py clean_duplicate_history [-m ...] --auto``

The -m flag is optional and is used to specify the amount of minutes to go back when searching for duplicate entries. This command can
be automated, e.g. by running a cronjob.