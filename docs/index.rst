.. pybinlock documentation master file, created by
   sphinx-quickstart on Fri Feb 28 21:54:50 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pybinhistory
============
*Because* ``pybinlog`` *was taken™*

``pybinhistory`` is a pypi package for the :mod:`binhistory` python library.

:mod:`binhistory` is a python library for programmatically reading and writing Avid bin history log (``.log``) files in 
multi-user Avid Media Composer projects.

.. caution::

   :mod:`binhistory` is an unofficial library created for educational purposes.  While the ``.log`` file format 
   is a very simple one, it is officially undocumented. Use this library at your own risk -- the developer assumes 
   no responsibility for any damage to your project, loss of data, or weird snippy drama about who threw the audio 
   out of sync in the latest version of the reel.

.. _bout-dem-logs:

About Avid bin logs
-------------------


An Avid bin log is a ``.log`` file that lives alongside an Avid bin (``.avb`` or ``.avs``) file in a multi-user 
Avid environment.  It maintains a history of the most recent modifications made to the contents of the bin.  Each time 
a user saves changes to a bin, its ``.log`` is updated with another entry.

By default, the log file contains a maximum of 10 log entries.  Each log entry contains:

- A timestamp of the modification
- The hostname of the system that made the modification
- The name of the user profile that made the modification

Here is an example ``.log`` file with the maximum 10 entries.  Hypothetically, if this were a log for an Avid bin 
called ``Sc 12.avb``, this log would live beside it as ``Sc 12.log``\.

.. code-block::
   :caption: ``Sc 12.log`` File Contents

   Fri Apr 28 18:46:21  Computer: zJimmy          User: Jimmy Edit     
   Fri Apr 28 19:07:25  Computer: zJimmy          User: Jimmy Edit     
   Fri Apr 28 19:39:47  Computer: zJimmy          User: Jimmy Edit     
   Tue May 02 18:04:03  Computer: zMichael        User: MJ 2021.12.2   
   Tue May 02 18:18:09  Computer: zMichael        User: MJ 2021.12.2   
   Thu Jun 01 11:55:36  Computer: zJimmy          User: Jimmy Edit     
   Mon Jun 12 13:27:10  Computer: zTimmy          User: user           
   Mon Jun 12 13:36:59  Computer: zTimmy          User: user           
   Tue Jun 27 17:22:13  Computer: zTootsie_LA     User: toot           
   Tue Jul 25 10:53:18  Computer: z_Michael       User: MJ 2021.12.2   


About :mod:`binhistory`
-----------------------

The :mod:`binhistory` library enables developers to safely create, read, and modify valid bin logs programmatically.

Interesting uses
----------------

- Be a good citizen!  Add a bin log entry when modifying a bin programmatically via automation/pipeline-y operations.
- Snoop around!  Easily gather metrics about modifications made by particular machines or users.
- Makes you look cool!  Everyone will be very impressed with you.  "Wow!" they'll say.

See :doc:`usage` for examples!

:mod:`binhistory` on the World Wide Web!
----------------------------------------

+---------------------+----------------------------------------------------------+
| PyPI Repository     | https://pypi.org/project/pybinhistory/                   |
+---------------------+----------------------------------------------------------+
| Github Repository   | https://github.com/mjiggidy/pybinhistory/                |
+---------------------+----------------------------------------------------------+
| Documentation       | https://pybinhistory.readthedocs.io/                     |
+---------------------+----------------------------------------------------------+


See also
--------

* `pybinlock <https://pybinlock.readthedocs.io>`_: A python library for locking and unlocking Avid bins

.. toctree:: 
   :maxdepth: 2
   :caption: Contents:
   
   installation
   quickstart
   usage
   api