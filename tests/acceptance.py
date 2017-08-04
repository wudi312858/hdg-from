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

from hdgfrom.cli import CLI
from hdgfrom.adapters import AdapterLibrary


class AcceptanceTests(TestCase):
    SWMM_OUTPUT = """
    Table - Node 3
                                Total Inflow    
    Days      	Hours    	(LPS)           
    0         	00:15:00  	0.18            
    0         	00:30:00  	2.30            
    0         	00:45:00  	2.06            
    """

    HDG_OUTPUT = """
    $GLLVHTTVDFile, V5.0
    $Creation Date: 03/31/2016 00:00
    $Waterbody Name: Unknown
    $Created by: Unknown
    $Start Date: 01/01/2017 12:00
    $End Date: 01/01/2017 12:00
    $Number of Data Lines: 3
    $X, Y, Station Height, Missing value,Profile Format, ExceFormat, Longitude, Latitude, Anemometer Height
    $Number of bins, Depth data type, TVD file type
    62000,6957300,0,999999999,0,0,0,0,0
    1,0,0
    1
    2,0,0,1.0,0,0.0,0.0,Flow Rate,Flow Rate
    $Year,Month,Day,Hour,Minute,Bin1,Flow Rate
    2017,1,1,0,15,0,0.18
    2017,1,1,0,30,0,2.30
    2017,1,1,0,45,0,2.06
    """

    SWMM_FILE = "my_swmm_file.txt"

    def setUp(self):
        self._create_file(self.SWMM_FILE, content=self.SWMM_OUTPUT)

    def teardown(self):
        self._delete_file(self.SWMM_FILE)
        self._delete_file(self._generated_file)

    @property
    def _generated_file(self):
        return self.SWMM_FILE.replace(".txt", ".hdg")

    def test_convertion_from_swmm(self):
        cli = CLI(AdapterLibrary())
        cli.run(["--format", "swmm", self.SWMM_FILE])
        self._verify_generated_file()

    def _create_file(self, file_name, content):
        with open(file_name, "w+") as output_file:
            output_file.write(content)

    def _delete_file(self, file_name):
        path = Path(file_name)
        path.unlink()

    def _verify_generated_file(self):
        path = Path(self._generated_file)
        self.assertTrue(path.exists())
        self.assertEqual(self.HDG_OUTPUT, path.read_text())
