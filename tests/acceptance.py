#
# HDG-from -- Generate HDG files for GEMSS
#
# Copyright (C) 2017 Di WU
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

# Compatibility with Pyhton 2.7
from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase
from mock import patch

from io import StringIO
from os import remove
from os.path import isfile
from datetime import datetime

from hdgfrom.cli import CLI, Display
from hdgfrom.adapters import AdapterLibrary


def fake_now():
    return datetime(2017, 1, 1, 12)


class AcceptanceTests(TestCase):
    SWMM_OUTPUT = ("Table - Node 3\n"
                   "                            Total Inflow\n"
                   "Days      	Hours    	(LPS)\n"
                   "0         	00:15:00  	0.18\n"
                   "0         	00:30:00  	2.30\n"
                   "0         	00:45:00  	2.06\n")

    HDG_OUTPUT = ("$GLLVHTTVDFile, V5.0\n"
                  "$Creation Date: 01/01/2017 12:00\n"
                  "$Waterbody Name: Node 3\n"
                  "$Created by: Unknown\n"
                  "$Start Date: 01/01/2017 12:00\n"
                  "$End Date: 01/01/2017 12:45\n"
                  "$Number of Data Lines: 3\n"
                  "$X, Y, Station Height, Missing value,Profile Format, ExceFormat, Longitude, Latitude, Anemometer Height\n"
                  "$Number of bins, Depth data type, TVD file type\n"
                  "62000,6957300,0,999999999,0,0,0,0,0\n"
                  "1,0,0\n"
                  "1\n"
                  "2,0,4,1.0,0,0.0,0.0,Flow Rate,Flow Rate\n"
                  "$Year,Month,Day,Hour,Minute,Bin1,Flow Rate\n"
                  "2017,1,1,12,15,0,15.55\n"
                  "2017,1,1,12,30,0,198.72\n"
                  "2017,1,1,12,45,0,177.98\n")

    SWMM_FILE = "my_swmm_file.txt"

    def setUp(self):
        self._create_file(self.SWMM_FILE, content=self.SWMM_OUTPUT)
        self._output = StringIO()
        self._cli = CLI(output=self._output)

    def teardown(self):
        self._delete_file(self.SWMM_FILE)
        self._delete_file(self._generated_file)

    @patch('hdgfrom.adapters.Writer.now', side_effect=fake_now)
    def test_convertion_from_swmm(self, mock):
        self._cli.run(["--format", "swmm", self.SWMM_FILE])

        self._verify_generated_file(self.HDG_OUTPUT)

        self._verify_output_contains(
            Display.INPUT_FILE_LOADED,
            file=self.SWMM_FILE,
            count=3)

        self._verify_output_contains(
            Display.CONVERSION_COMPLETE,
            file=self._generated_file)

    @patch('hdgfrom.adapters.Writer.now', side_effect=fake_now)
    def test_setting_user_name(self, mock):
        user_name = "James Brown"
        self._cli.run(["--user-name", user_name, self.SWMM_FILE])

        self._verify_generated_file(
            self.HDG_OUTPUT.replace("Unknown", user_name))

        self._verify_output_contains(
            Display.CONVERSION_COMPLETE,
            file=self._generated_file)

    @patch('hdgfrom.adapters.Writer.now', side_effect=fake_now)
    def test_setting_water_body_name(self, mock):
        water_body = "Havre de Rotheneuf"
        self._cli.run(["--water-body", water_body, self.SWMM_FILE])

        self._verify_generated_file(
            self.HDG_OUTPUT.replace("Node 3", water_body))

        self._verify_output_contains(
            Display.CONVERSION_COMPLETE,
            file=self._generated_file)

    @patch('hdgfrom.adapters.Writer.now', side_effect=fake_now)
    def test_setting_hdg_file_name(self, mock):
        file_name = "bidon.hdg"
        self._cli.run(["--output", file_name, self.SWMM_FILE])

        self._verify_generated_file(
            self.HDG_OUTPUT,
            file_name)

        self._verify_output_contains(
            Display.CONVERSION_COMPLETE,
            file=file_name)

    @patch('hdgfrom.adapters.Writer.now', side_effect=fake_now)
    def test_unit_conversion(self, mock):
        unit = "CMD"
        self._cli.run(["--unit", unit, self.SWMM_FILE])

        self._verify_generated_file(
            "$GLLVHTTVDFile, V5.0\n"
            "$Creation Date: 01/01/2017 12:00\n"
            "$Waterbody Name: Node 3\n"
            "$Created by: Unknown\n"
            "$Start Date: 01/01/2017 12:00\n"
            "$End Date: 01/01/2017 12:45\n"
            "$Number of Data Lines: 3\n"
            "$X, Y, Station Height, Missing value,Profile Format, ExceFormat, Longitude, Latitude, Anemometer Height\n"
            "$Number of bins, Depth data type, TVD file type\n"
            "62000,6957300,0,999999999,0,0,0,0,0\n"
            "1,0,0\n"
            "1\n"
            "2,0,4,1.0,0,0.0,0.0,Flow Rate,Flow Rate\n"
            "$Year,Month,Day,Hour,Minute,Bin1,Flow Rate\n"
            "2017,1,1,12,15,0,15.55\n"
            "2017,1,1,12,30,0,198.72\n"
            "2017,1,1,12,45,0,177.98\n",
            self._generated_file)

        self._verify_output_contains(
            Display.CONVERSION_COMPLETE,
            file=self._generated_file)

    @patch('hdgfrom.adapters.Writer.now', side_effect=fake_now)
    def test_detecting_all_zero_flows(self, mock):
        self._cli.run(["--unit", "CMS", self.SWMM_FILE])

        self._verify_output_contains(
            Display.WARNING_ALL_ZERO_FLOW.format(unit="CMS"))

        
    def test_invalid_start_date(self):
        date = "this-is-not-a-valid-date!"
        self._cli.run(["--start-date", date, self.SWMM_FILE])

        self._verify_output_contains(
            Display.ERROR_INVALID_DATE,
            date=date)

    def test_converting_a_file_that_does_not_exist(self):
        file_name = "does-not-exist.txt"

        self._cli.run(["--format", "swmm", file_name])

        self._verify_output_contains(
            Display.ERROR_INPUT_FILE_NOT_FOUND,
            file=file_name,
            hint="No such file or directory")

    @property
    def _generated_file(self):
        return self.SWMM_FILE.replace(".txt", ".hdg")

    def _create_file(self, file_name, content):
        with open(file_name, "w+") as output_file:
            output_file.write(content)

    def _delete_file(self, file_name):
        remove(file_name)

    def _verify_output_contains(self, text, **arguments):
        output = self._output.getvalue()
        expected_text = text.format(**arguments)
        self.assertTrue(expected_text in output, msg=output)

    def _verify_generated_file(self, expected_content, path=None):
        file_path = path or self._generated_file
        self.assertTrue(isfile(file_path))
        with open(file_path, "r") as generated_file:
            generated_text = generated_file.read()
            self.assertEqual(expected_content, generated_text, msg=generated_text)
