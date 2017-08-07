#
# hdg-from -- Generate HDG files for GEMSS
#
# Copyright (C) 2017 Di WU
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

# Compatibility with Pyhton 2.7
from __future__ import absolute_import, division, print_function, unicode_literals

from io import StringIO
from unittest import TestCase
from datetime import timedelta

from hdgfrom.flow import Flow, Observation, Rate
from hdgfrom.adapters import SWMMReader, HDGWriter


class SWMMReaderTests(TestCase):

    SWMM_TEXT = """
    Table - Node 3
                                Total Inflow
    Days      	Hours     	(LPS)
    0         	00:15:00  	0.18
    0         	00:30:00  	2.30
    0         	00:45:00  	2.06
    """

    def setUp(self):
        self._reader = SWMMReader()
        self._stream = StringIO(self.SWMM_TEXT)

    def test_extract_water_body(self):
        flow = self._reader.read_from(self._stream)
        self.assertEqual("Node 3", flow.water_body)

    def test_extract_observations(self):
        flow = self._reader.read_from(self._stream)
        self.assertEqual(3, len(flow.observations))
        self.assertEqual([0.18, 2.30, 2.06],
                         [o.rate.value for o in flow.observations])
        self.assertEqual([15*60, 30*60, 45*60],
                 [o.time.total_seconds() for o in flow.observations])


class HDGWriterTest(TestCase):

    def setUp(self):
        self._writer = HDGWriter()
        self._output = StringIO()
        self._flow = Flow(
            "Test Water",
            [ Observation(Rate(0.10), timedelta(minutes=15)),
              Observation(Rate(0.20), timedelta(minutes=30)),
              Observation(Rate(0.30), timedelta(minutes=45)) ])
        self._expected_hdg = ("$GLLVHTTVDFile, V5.0\n"
                              "$Creation Date: 03/31/2016 00:00\n"
                              "$Waterbody Name: Test Water\n"
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
                              "2017,1,1,12,15,0,0.10\n"
                              "2017,1,1,12,30,0,0.20\n"
                              "2017,1,1,12,45,0,0.30\n")

    def test_write(self):
        self._writer.write_to(self._flow, self._output)
        self.assertEqual(self._expected_hdg, self._output.getvalue())

