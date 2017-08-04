#
# hdg-from -- Generate HDG files for GEMSS
#
# Copyright (C) 2017 Di WU
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

from unittest import TestCase
from datetime import datetime

from hdgfrom.flow import Flow, Rate, Observation


class EmptyFlowTests(TestCase):

    def setUp(self):
        self._flow = Flow()

    def test_has_water_body(self):
        self.assertTrue(self._flow.water_body, Flow.DEFAULT_WATER_BODY)

    def test_rate_at(self):
        self.assertEqual(None, self._flow.rate_at(datetime.now()))

    def test_observations_are_empty(self):
        self.assertEqual([], self._flow.observations)


class FlowTests(TestCase):

    def setUp(self):
        date_format = "%d/%m/%y %H:%M"
        observations = [
            Observation(Rate(0.25), datetime.strptime("16/09/81 16:40", date_format)),
            Observation(Rate(0.50), datetime.strptime("16/09/81 16:40", date_format))
        ]
        self._flow = Flow(
            water_body="Test",
            observations=observations)

    def test_observations(self):
        self.assertEqual(2, len(self._flow.observations))


class RateTests(TestCase):

    def test_get_value(self):
        value = 0.89
        rate = Rate(value)
        self.assertEqual(value, rate.value)

    def test_reject_negative_value(self):
        with self.assertRaises(ValueError):
            rate = Rate(-4.56)


class ObservationTests(TestCase):

    def setUp(self):
        self._rate = Rate(0.25)
        self._time = datetime(
            year=2017,
            month=7,
            day=4,
            hour=10,
            minute=42,
            second=21)
        self._observation = Observation(self._rate, self._time)

    def test_get_rate(self):
        self.assertEqual(self._rate, self._observation.rate)

    def test_get_time(self):
        self.assertEqual(self._time, self._observation.time)
