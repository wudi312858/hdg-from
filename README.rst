hdg-from |---| Generate HDG files for GEMSS
===========================================

.. image:: https://img.shields.io/pypi/v/hdgfrom.svg
   :target: https://pypi.python.org/pypi/hdgfrom

"hdg-from" is a simple command-line tool that generates HDG files for
the Global Environment Modelling System for Subsurface waters
(GEMSS_).

Usage Example
-------------

For instance, if you have data produced by the Storm Water Management
Model (SWMM_), say in a text file ``my-data.txt`` in for instance,
where the flow rates are in liters per second (LPS), as follows:

.. code-block:: text

    Table - Node 1
                                Total Inflow
    Days      	Hours    	(LPS)
    0         	00:15:00  	0.18
    0         	00:30:00  	2.30
    0         	00:45:00  	2.06

You can use `hdg-from` to obtain the equivalent HDG file by entering.

.. code-block:: console

    $ hdg-from my-data.txt
    3 observation(s) loaded from 'my-data.txt'.
    'my-data.hdg' successfully generated.

In the generated file, named by default ``my-data.hdg``, the flow
values have been convert to cubic meters per day (CMD).

.. code-block:: text

    $GLLVHTTVDFile, V5.0
    $Creation Date: 09/08/2017 08:52
    $Waterbody Name: Node 1
    $Created by: Unknown
    $Start Date: 01/01/2017 12:00
    $End Date: 01/01/2017 12:45
    $Number of Data Lines: 3
    $X, Y, Station Height, Missing value,Profile Format, ExceFormat, Longitude, Latitude, Anemometer Height
    $Number of bins, Depth data type, TVD file type
    62000,6957300,0,999999999,0,0,0,0,0
    1,0,0
    1
    2,0,4,1.0,0,0.0,0.0,Flow Rate,Flow Rate
    $Year,Month,Day,Hour,Minute,Bin1,Flow Rate
    2017,1,1,12,15,0,15.55
    2017,1,1,12,30,0,198.72
    2017,1,1,12,45,0,177.98

Below are the options that `hdg-from` accepts:

-f <format>, --format <format>

    The file format of the input file. So far only the SWMM format is
    available, but other may be supported in later versions.

-n <name>, --user-name <name>

    The name of the user that creates the HDG file (see HDG Field
    ``Created By``). Should be enclosed in double quotes if it
    contains space. By default, the user name is "Unknown".

-o <file>, --output <file>

    The HDG file to generate. By default, the generated file will have
    the same name as the given input file (only its extension will
    differ), as in the example above.

-s <date>, --start-date <date>

    The date used as a starting point to convert simulated time into
    absolute time (see HDG Field ``State Date``). Dates must adhere to
    the `ISO 8601`_ standard such as 2017-01-01T12:00:00. By default,
    the date used is Jan. 1, 2017 at 12:00 AM.

--unit <unit>

    The flow rate unit that should be used in the HDG file. By
    default, HDG files use cubic meter per day (CMD), but the other
    options are:

    - "CMS" for cubic meters per seconds
    - "CFS" for cubic feet per seconds
    - "MGD" for millions of gallon per day
    - "GPM" for gallons per minutes
    - "CMD" for cubic meters per day
    - "CMH" for cubic meters per hour

-w <name>, --water-body <name>

    The name of the water body to set in the HDG file (see Field
    ``Waterbody Name``). This will override the one read in the SWMM
    file, if any. Should be enclosed in double quotes if it contains
    spaces. By default, the name of the water body is read from the
    input file.

-h, --help

    Show a similar description of the available options and exit.


Installation
------------

`hdg-from` is a simple Python 3.3+ application (also tested on Python
2.7) with no additional dependency. To install the *latest stable
release* from the Pypi_ repository, the simplest way is to use ``pip``
as follows:

.. code-block:: console

   $ pip install hdgfrom

Alternatively, you may want to install the *latest version under
development*. To this end, ``pip`` you can directly install the last
commit on the Git repository, using:

.. code-block:: console

   $ pip install git+https://github.com/wudi312858/hdg-from


Change Log
----------
:Version 0.3.0:
 - Unit conversions from the SWMM file to the HDG file.
 - Warn about conversions that lead to only zero values.

:Version 0.2.0:
 - Let the user specify the name of the generated HDG file.
 - Let the user specify its name for inclusion in the HDG file.
 - Let the user override the name of the water body.
 - Tell the user how many observations were loaded from the input
   file.
 - Catch `FileNotFoundError` properly.
 - Catch invalid start dates properly.
 - Generate the correct creation date.
 - Compatibility with Python 2.7 and Python 3.3+.

:Version 0.1.0:
 - Accepts text files generated by SWMM_ and generates an equivalent
   HDG file.
 - Let the user specify the starting date to convert simulated time
   into absolute time.
 - Only tested on Python 3.6.

.. |---| unicode:: U+2014

.. _GEMSS: http://gemss.com/gemss.html
.. _SWMM: https://en.wikipedia.org/wiki/Storm_Water_Management_Model
.. _sources: https://github.com/wudi312858/hdg-from/archive/master.zip
.. _PIP: https://en.wikipedia.org/wiki/Pip_(package_manager)
.. _`ISO 8601`: https://en.wikipedia.org/wiki/ISO_8601
.. _Pypi: https://pypi.python.org/pypi
