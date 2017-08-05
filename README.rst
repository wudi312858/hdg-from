hdg-from |---| Generate HDG files for GEMSS
===============================================

"hdg-from" is a simple command-line tool that generates HDG files for
the Global Environment Modelling System for Subsurface waters
(GEMSS_).

Example
-------

For instance, if you have data produced by the Storm Water
Management Model (SWMM_), say in a text file in for instance, you can
use `hdg-from` to obtain the equivalent HDG file by entering.

.. code-block:: console

    $> hdg-from --format swmm my-data.txt

Below are the options that `hdg-from` accepts:

+---------------+-------------------------------------+---------------------+
| Options       | Description                         | Default Value       |
+===============+=====================================+=====================+
| -f,           |The file format of the input file    | swmm                |
| --format      |                                     |                     |
+---------------+-------------------------------------+---------------------+
| -sd,          |Start date used to convert simulated | 2017-01-01T12:00:00 |
| --start-date  |time in ISO 8601                     |                     |
|               |(i.e., YYYY-MM-DDThh:mm:ss)          |                     |
+---------------+-------------------------------------+---------------------+
| -h,           |Display a the list of options and    |N/A                  |
| --help        |exit                                 |                     |
+---------------+-------------------------------------+---------------------+

Installation
------------

`hdg-from` is a simple Python 3 application with no additional
dependency. To install it, simply download the sources_, unzip them in
a directory of your choice and use pip to install it. Here are the
needed commands you may enter:

.. code-block:: console

   $> wget https://github.com/wudi312858/hdg-from/archive/master.zip
   $> unzip master.zip
   $> cd hdg-from
   $> pip install -e i.

.. |---| unicode:: U+2014

.. _GEMSS: http://gemss.com/gemss.html
.. _SWMM: https://en.wikipedia.org/wiki/Storm_Water_Management_Model
.. _sources: https://github.com/wudi312858/hdg-from/archive/master.zip
