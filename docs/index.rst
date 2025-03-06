.. pybinlock documentation master file, created by
   sphinx-quickstart on Fri Feb 28 21:54:50 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

###########
pybinhistory
###########
*Because ``pybinlog`` was taken™*

``pybinlog`` is a pypi package for the :mod:`binhistory` python library.

:mod:`binhistory` is a python library for programmatically reading and writing Avid bin logs (``.log``) files in 
Avid Media Composer projects.

.. caution::

   :mod:`binhistory` is an unofficial library created for educational purposes.  While the ``.log`` file format 
   is a very simple one, it is officially undocumented. Use this library at your own risk -- the developer assumes 
   no responsibility for any damage to your project, loss of data, or weird snippy drama about who threw the audio 
   out of sync in the latest version of the reel.

About Avid bin logs
===================

An Avid bin log is a ``.log`` file that lives alongside an Avid bin (``.avb`` or ``.avs``) file in a multi-user 
Avid environment.  It maintains a history of the most recent modifications made to the contents of the bin.

By default, the log file contains a maximum of 10 log entries.  Each log entry contains:

- A timestamp of the modification
- The hostname of the system that made the modification
- The name of the user profile that made the modification

About :mod:`binhistory`
=======================

The :mod:`binhistory` library enables developers to safely create, read, and modify valid bin logs programmatically.

Interesting uses
----------------

- Be a good citizen!  Add a bin log entry when modifying a bin programmatically via automation/pipeline-y operations.
- Snoop around!  Easily gather metrics about modifications made by particular machines or users.
- Makes you look cool!  Everyone will be very impressed with you.  "Wow!" they'll say.

See :doc:`usage` for examples!

See also
--------

* `pybinlock <https://pybinlock.readthedocs.io>`_: A python library for locking and unlocking Avid bins

.. toctree:: 
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   api