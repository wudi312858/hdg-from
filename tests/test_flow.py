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
from datetime import datetime

from hdgfrom.flow import Flow, Rate


class EmptyFlowTests(TestCase):

    def setUp(self):
        self._flow = Flow()

    def test_has_water_body(self):
        self.assertTrue(self._flow.water_body, Flow.DEFAULT_WATER_BODY)

    def test_rate_at(self):
        self.assertEqual(None, self._flow.rate_at(datetime.now()))


class RateTests(TestCase):

    def test_get_value(self):
        value = 0.89
        rate = Rate(value)
        self.assertEqual(value, rate.value)

    def test_reject_negative_value(self):
        with self.assertRaises(ValueError):
            rate = Rate(-4.56)
