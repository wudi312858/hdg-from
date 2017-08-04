#
# hdg-from -- Generate HDG files for GEMSS
#
# Copyright (C) 2017 Di WU
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license. See the LICENSE file for details.
#


class Rate:

    ERROR_INVALID_RATE = "Rate cannot be negative, but found (value={})"

    def __init__(self, value):
        if value < 0:
            message = self.ERROR_INVALID_RATE.format(value)
            raise ValueError(message)

        self._value = value

    @property
    def value(self):
        return self._value


class Observation:

    def __init__(self, rate, time):
        self._rate = rate
        self._time = time

    @property
    def rate(self):
        return self._rate

    @property
    def time(self):
        return self._time


class Flow:

    DEFAULT_WATER_BODY = "Unknown"

    def __init__(self, water_body=None, observations=[]):
        self._water_body = water_body or self.DEFAULT_WATER_BODY
        self._observations = observations

    @property
    def water_body(self):
        return self._water_body

    @property
    def observations(self):
        return self._observations

    def rate_at(self, time):
        return None
