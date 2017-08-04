# hdg-from &mdash; Generate HDG files for GEMSS

`hdg-from` is a simple command-line tools that generates HDG file for
the
[Global Environment Modelling System for Subsurface waters (GEMSS)](http://gemss.com/gemss.html).


## Example
For instance, if you have data produced by
the
[Storm Water Management Model (SWMM)](https://en.wikipedia.org/wiki/Storm_Water_Management_Model) for
instance, in a text file, you can use `hdg-from`to obtain the
equivalent HDG file by entering:

	$> hdg-from --format swmm my-data.txt 
	
Below are the options that `hdg-from` accepts:

| Options | Description | Default Value |
|---------|-------------|---------------|
| -f, --format| The file format of the input file | swmm |
| -sd, --start-date|Start date used to convert timestamp (i.e., YYYY-MM-DDThh:mm:ss"| 2017-01-01T12:00:00|
| -h, --help | Display a the list of options and exit | N/A |


## Installation

`hdg-from`is a simple Python 3 application with no additional
dependency. To install it, simply download the sources, unzip them in
a directory of your choice and use pip to install it. Here are the
needed commands you may enter:

	$> wget https://github.com/wudi312858/hdg-from/archive/master.zip
	$> unzip master.zip
	$> cd hdg-from
	$> pip install -e i.

