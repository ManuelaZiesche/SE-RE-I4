Cronjobs
--------

In the following lines there is an explanation how to create cronjobs to
schedule tasks. These tasks help to cleanup the database of the application.

First make sure you have installed cron than you can add cronjobs
with the command:

  ``crontab -e``

Now you can see a file like this:

.. code-block:: bash

  # Edit this file to introduce tasks to be run by cron.
  #
  # Each task to run has to be defined through a single line
  # indicating with different fields when the task will be run
  # and what command to run for the task
  #
  # To define the time you can provide concrete values for
  # minute (m), hour (h), day of month (dom), month (mon),
  # and day of week (dow) or use '*' in these fields (for 'any').
  #
  # Notice that tasks will be started based on the cron's system
  # daemon's notion of time and timezones.
  #
  # Output of the crontab jobs (including errors) is sent through
  # email to the user the crontab file belongs to (unless redirected).
  #
  # For example, you can run a backup of all your user accounts
  # at 5 a.m every week with:
  # 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
  #
  # For more information see the manual pages of crontab(5) and cron(8)
  #
  # m h  dom mon dow   command

At the bottom of the file you can add your personal cronjobs.
To keep it simple our recommendation is to create a script with all commands you
want (described in the commands section of the code documentation).
You can easily schedule this script to run once a week with cronjob.

  ``0 0 * * 0 bash /path/to/script``
