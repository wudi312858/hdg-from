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

from unittest import TestCase
from datetime import datetime

from hdgfrom.flow import Flow, Rate, Observation, Unit


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
            Observation(Rate(0.25, Unit.CMH),
                        datetime.strptime("16/09/81 16:40", date_format)),
            Observation(Rate(0.50, Unit.CMH),
                        datetime.strptime("16/09/81 16:40", date_format))
        ]
        self._flow = Flow(
            water_body="Test",
            observations=observations)

    def test_observations(self):
        self.assertEqual(2, len(self._flow.observations))

    def test_convert_to(self):
        converted = self._flow.convert_to(Unit.CMD)
        for i, each_observation in enumerate(converted.observations):
            self.assertEqual(24 * self._flow.observations[i].rate.value,
                             each_observation.rate.value)


class RateTests(TestCase):

    def setUp(self):
        self._value = 0.5
        self._unit = Unit.LPS
        self._rate = Rate(self._value, self._unit)

    def test_get_value(self):
        self.assertEqual(self._value, self._rate.value)

    def test_reject_negative_value(self):
        with self.assertRaises(ValueError):
            rate = Rate(-4.56)

    def test_conversion_to_lps(self):
        new_rate = self._rate.convert_to(Unit.LPS)
        self.assertAlmostEqual(self._rate.value, new_rate.value,
                               delta=1e-6)

    def test_conversion_to_cmd(self):
        new_rate = self._rate.convert_to(Unit.CMD)
        self.assertAlmostEqual(self._rate.value * 86.4, new_rate.value,
                               delta=1e-6)

    def test_cmd_to_lps(self):
        rate = Rate(0.25, Unit.CMD)
        new_rate = rate.convert_to(Unit.LPS)
        self.assertAlmostEqual(0.25 / 86.4, new_rate.value,
                               delta=1e-6)


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

