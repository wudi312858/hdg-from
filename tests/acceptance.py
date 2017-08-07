#
# HDG-from -- Generate HDG files for GEMSS
#
# Copyright (C) 2017 Di WU
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from unittest import TestCase
from pathlib import Path
from io import StringIO

from hdgfrom.cli import CLI, Display
from hdgfrom.adapters import AdapterLibrary


class AcceptanceTests(TestCase):
    SWMM_OUTPUT = ("Table - Node 3\n"
                   "                            Total Inflow\n"
                   "Days      	Hours    	(LPS)\n"
                   "0         	00:15:00  	0.18\n"
                   "0         	00:30:00  	2.30\n"
                   "0         	00:45:00  	2.06\n")

    HDG_OUTPUT = ("$GLLVHTTVDFile, V5.0\n"
                  "$Creation Date: 03/31/2016 00:00\n"
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
                  "2,0,0,1.0,0,0.0,0.0,Flow Rate,Flow Rate\n"
                  "$Year,Month,Day,Hour,Minute,Bin1,Flow Rate\n"
                  "2017,1,1,12,15,0,0.18\n"
                  "2017,1,1,12,30,0,2.30\n"
                  "2017,1,1,12,45,0,2.06\n")

    SWMM_FILE = "my_swmm_file.txt"

    def setUp(self):
        self._create_file(self.SWMM_FILE, content=self.SWMM_OUTPUT)
        self._output = StringIO()
        self._cli = CLI(output=self._output)

    def teardown(self):
        self._delete_file(self.SWMM_FILE)
        self._delete_file(self._generated_file)

    def test_convertion_from_swmm(self):
        self._cli.run(["--format", "swmm", self.SWMM_FILE])

        self._verify_generated_file()

        expected = Display.INPUT_FILE_LOADED.format(
            file=self.SWMM_FILE,
            count=3)
        self._verify_output_contains(expected)

    def test_converting_a_file_that_does_not_exist(self):
        file_name = "does-not-exist.txt"

        self._cli.run(["--format", "swmm", file_name])

        expected = Display.ERROR_INPUT_FILE_NOT_FOUND.format(
            file=file_name,
            hint="No such file or directory")
        self._verify_output_contains(expected)

    @property
    def _generated_file(self):
        return self.SWMM_FILE.replace(".txt", ".hdg")

    def _create_file(self, file_name, content):
        with open(file_name, "w+") as output_file:
            output_file.write(content)

    def _delete_file(self, file_name):
        path = Path(file_name)
        path.unlink()

    def _verify_output_contains(self, text):
        output = self._output.getvalue()
        self.assertTrue(text in output, msg=output)

    def _verify_generated_file(self):
        path = Path(self._generated_file)
        self.assertTrue(path.exists())
        generated_text = path.read_text()
        #print(self.HDG_OUTPUT, "\n\n", generated_text)
        self.assertEqual(self.HDG_OUTPUT, generated_text)
