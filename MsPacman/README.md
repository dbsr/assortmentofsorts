MsPacman Package Auditor
========================

MsPacman is a package auditor. I am not competely sure what
an auditor exactly is.

MsPacman can help you to get a better idea about what packages
are currently installed.
You can use MsPacman to select packages you would like to remove and let
MsPacman save them to a text file which subsequently can be used by pacman
to perform the actual removal.

Features I'd like to add are graphical representations of dependency relations
between different packages and a custom 'categorizer' using tagwords from 
the package descriptions.



Requirements
------------

MsPacman uses [expac](https://github.com/falconindy/expac) to gather 
information about the packages installed on your system.


Installation
------------

  pip install git+https://github.com/dbsr/MsPacman.git


Usage
-----

    $ mspacman

        -h / --host HOST ADDRESS (127.0.0.1)

        -p / --port PORT (5555)

        -o / --output-file OUTPUT FILE (~/mspacman.cmd)


Screenshot
----------

![screenshot](http://www.daanmathot.nl/static/img/mspacman_ss.png)
