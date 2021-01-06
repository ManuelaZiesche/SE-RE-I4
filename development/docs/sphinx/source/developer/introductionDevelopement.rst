Introduction Development
-------------------------

This and the following sections deal with development specific topics.

Clone the Git-Repository, install the requirements and fire up the Webserver for developement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Requirements:

* A installation of git
* A Installation of Python (we used 3.8.2)
* (optional) a installation of virtualenviroment
* A Webbrowser

First step is to pull the Git-Repository

    ``git clone https://github.com/mribrgr/StuRa-Mitgliederdatenbank.git``

Next we change the directory to the pulled Git-Repository with:

    ``cd StuRa-Mitgliederdatenbank/``

Now we need to install all python requirements (optional: install it in a virtualenviroment).
You can use the requirements.txt, it contains all requirements we used.

    ``pip install -r requirements.txt``

The Basics are done, now we need to create a Database and apply all migrations to it. We use the
makemigrations and the migrate command from the manage.py.

    | ``python3 ./manage.py makemigrations``
    | ``python3 ./manage.py migrate``

If the Database was successfully created there must be a db.sqlite3 in the directory.
As last step, before we can fire up the server, we need to create an admin account
using the command superuser so that we can login into the application.

    ``python3 ./manage.py createsuperuser``

Now we can start the server by typing:

    ``python3 ./manage.py runserver``
