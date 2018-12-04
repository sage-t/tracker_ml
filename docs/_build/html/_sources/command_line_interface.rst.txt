.. _command_line_interface:

************
CLI Tool
************

tracker.ml command line interface for locally tracking/reverting file changes and tracking results
for each change. Similar to git, but works with the SDK to track every time a new model is
trained/tested.


Examples
=========

Use the help command::

    $ tracker --help
    $ tracker status --help


Initialize in the project root and optionally login to www.tracker.ml::

    $ tracker init -u <username> -p <password> -n <project name>


Add file(s)/directory(s) that will be saved every run::

    $ tracker add .


Stop recording file(s)/directory(s) that would be saved every run::

    $ tracker remove .


View past trials and sort them::

    $ tracker status
    $ tracker status -k accuracy -l 2 -r


Reset tracked files to specified version::

    $ tracker deploy 3


Undo or redo file change between past runs::

    $ tracker undo
    $ tracker redo

Push tracked parameters and file versions to www.tracker.ml if not done with the sdk::

    $ tracker push