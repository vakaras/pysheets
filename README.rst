==============
Python starter
==============

**Python starter** is a generic template for creating Python libraries
and applications.

Structure
=========

+   ``bin`` – directory, where scripts are placed.
+   ``src`` – directory, where package code is placed.
+   ``LICENCE.txt`` – LGPL license text.
+   ``README.rst``.
+   ``CHANGES.txt``.
+   ``setup.cfg`` – `setup configuration file 
    <http://docs.python.org/distutils/configfile.html>`_.
+   ``setup.py`` – `description
    <http://docs.python.org/distutils/introduction.html>`_.
+   ``bootstrap.py``.

+   ``docs`` – directory, where package documentation is placed.
+   ``Makefile``
+   ``buildout.cfg``

Tools
=====

+   *buildout* – isolated environment;
+   *pylint* – code quality checker;
+   *sphinx* and *rst2pdf* – for documentation;
+   *rmtoo* – requirements management tool;
+   *nose* – for testing.
+   `chaoflow.testing.ipython
    <http://pypi.python.org/pypi/chaoflow.testing.ipython/0.4>`_ – for
    interactive doctest writing.

Scripts
=======

+   ``bin/start`` – script, that prepares environment for new project.

How to start
============

#.  Clone template:

    .. code-block:: bash

        git clone git://github.com/vakaras/Python-Starter.git ${PROJECT}

    Here ``${PROJECT}`` is the directory name of your project.

#.  Change default repository. Assuming you are in project directory:

    .. code-block:: bash

        git remote rename origin template
        git remote add origin ${REPOSITORY}
        git push -u origin master

    Here ``${REPOSITORY}`` is the URL of your public repository (at 
    `github <github.com>`_ or somewhere else).

#.  Replace ``README.rst`` with yours.
#.  Start:

    .. code-block:: bash

        python3 bin/start ${APP_NAME} ${AUTHOR} ${AUTHOR_EMAIL}

    Example:

    .. code-block:: bash

        python3 bin/start db-utils \
            "Vytautas Astrauskas" \
            vastrauskas@gmail.com

#.  Buildout:
    
    .. code-block:: bash

        make buildout

    If you get error like:

    .. code-block:: bash

        Creating /usr/local/lib/python2.6/dist-packages/setuptools-0.6c11-py2.6.egg-info
        error: /usr/local/lib/python2.6/dist-packages/setuptools-0.6c11-py2.6.egg-info: Permission denied
        An error occurred when trying to install distribute 0.6.19. Look above this message for any errors that were output by easy_install.
        While:
          Installing.
          Checking for upgrades.
          Getting distribution for 'distribute'.
        Error: Couldn't install: distribute 0.6.19

    Then you can install distribute into your home directory:

    .. code-block:: bash

        CURRENT_LOC=`pwd`
        cd /tmp
        wget -c http://pypi.python.org/packages/source/d/distribute/distribute-0.6.19.tar.gz
        tar -xvf distribute-*.tar.gz 
        cd distribute*
        python setup.py install --user
        cd "$CURRENT_LOC"

    After that, rerun buildout:

    .. code-block:: bash

        rm -rf bin/buildout parts/
        make buildout

If you want to update template:

.. code-block:: bash
    
    git pull template master

If you want to include library created with this template into another
project, just add egg name into projects ``buildout.cfg`` and
URL of your repository in ``[sources]`` section, like this:

.. code-block:: cfg

    [buildout]
    ...
    eggs =
        ...
        db-utils

    ... 

    [sources]
    db-utils = git git://github.com/vakaras/db-utils.git
    ...


Requirements
============

+   **Python3**

In Ubuntu you can install everything with command:

.. code-block:: bash

    sudo apt-get install python3 
