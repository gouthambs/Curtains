Curtains
========

Curtains is a command line tool for remote execution, application deployment and
system administration in the Windows environment (as of now) without using SSH.
The Curtains API brings some of the niceties of `fabric <http://www.fabfile.org/>`_
API but with native Windows powershell.

Installation
============

To install curtains:

    pip install curtains

or

    easy_install curtains


Quickstart
==========

.. code:: python

    # curtfile.py
    from curtains.api import task

    @task()
    def hello_world():
        from curtains.api import local, run
        local("echo Hello World!")



Save this file and when you invoke the following command from the same path as this file:

    curt