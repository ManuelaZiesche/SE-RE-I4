Update the Application
----------------------

This section describes how to update the application from an existing deployment.


Update From GitHub with no changes in migrations:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First you need to get the ownership back from www-data.
In my example my user is *pi* and the application is locatetd
in pi's home directory.

  | ``sudo chown pi:pi ~/StuRa-Mitgliederdatenbank/db.sqlite3``
  | ``sudo chown pi:pi ~/StuRa-Mitgliederdatenbank``

Now we need to stash our changes we have done during our config.

  ``git stash``

We can now pull the latest version from the git Repository

  ``git pull``

To apply our configs back we need to get them back from the stash

  ``git stash pop``

At last you need to give the ownership back to www-data.
  | ``sudo chown www-data:www-data ~/StuRa-Mitgliederdatenbank/db.sqlite3``
  | ``sudo chown www-data:www-data ~/StuRa-Mitgliederdatenbank``
