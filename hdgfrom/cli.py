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

from argparse import ArgumentParser
from datetime import datetime
from sys import argv, stdout

from hdgfrom.flow import Flow
from hdgfrom.adapters import FileFormats, AdapterLibrary


class Arguments:
    """
    Encapsulate the arguments received from the command line
    """

    @staticmethod
    def read_from(command_line):
        parser = Arguments._prepare_parser()
        arguments = parser.parse_args(command_line)
        return Arguments(
            input_file=arguments.input_file,
            input_format=arguments.format,
            start_date=arguments.start_date
        )

    @staticmethod
    def _prepare_parser():
        parser = ArgumentParser(
            "hdg-from",
            description="Generate HDG file for GEMSS")
        parser.add_argument(
            "input_file",
            help="The file that must be converted to HDG")
        parser.add_argument(
            "-f",
            "--format",
            choices=["swmm"],
            default="swmm",
            help="Format of the input file")
        parser.add_argument(
            "-sd", "--start-date",
            default="2017-1-1T12:00:00",
            help="Start date used to convert timestamp (i.e., YYYY-MM-DDThh:mm:ss")
        return parser

    def __init__(self, input_file, input_format, start_date):
        self._input_file = input_file
        self._input_format = FileFormats.match(input_format)
        self._start_date = self._validate(start_date)

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    ERROR_INVALID_DATE = ("Invalid date '{text}'.\n"
                          "Use ISO8601 format (e.g., 1982-05-05T12:050:34)")

    @staticmethod
    def _validate(text):
        try:
            return datetime.strptime(text, Arguments.DATE_FORMAT)
        except ValueError:
            message = ERROR_INVALID_DATE.format(text=text)

    @property
    def input_file(self):
        return self._input_file

    @property
    def input_format(self):
        return self._input_format

    @property
    def output_file(self):
        return self._input_file.replace(".txt", ".hdg")

    @property
    def start_date(self):
        return self._start_date


class Display:
    """
    Encapsulate printing messages on the console.
    """

    INPUT_FILE_LOADED = (
        "{count} observation(s) loaded from '{file}'.\n"
    )

    CONVERSION_COMPLETE = (
        "'{file}' successfully generated.\n"
    )

    ERROR_INPUT_FILE_NOT_FOUND = (
        "Error: Unable to open the input file '{file}'.\n"
        "       {hint}\n"
    )

    def __init__(self, output):
        self._output = output or stdout

    def input_file_loaded(self, arguments, flow):
        self._display(self.INPUT_FILE_LOADED,
                      file=arguments.input_file,
                      count=len(flow.observations))

    def conversion_complete(self, arguments):
        self._display(self.CONVERSION_COMPLETE,
                      file=arguments.output_file)

    def input_file_not_found(self, arguments, error):
        self._display(self.ERROR_INPUT_FILE_NOT_FOUND,
                      file=arguments.input_file,
                      hint=error.strerror)

    def _display(self, message, **arguments):
        text = message.format(**arguments)
        self._output.write(text)


class CLI:
    """
    Parse the command line and then read the flow from the input file,
    and write the same flow down as an HDG file.
    """

    def __init__(self, adapters=None, output=None):
        self._adapters = adapters or AdapterLibrary()
        self._display = Display(output)

    def run(self, command_line):
        try:
            arguments = Arguments.read_from(command_line)

            flow = self._read_flow_from(arguments.input_format, arguments.input_file)
            self._display.input_file_loaded(arguments, flow)

            flow.start_date = arguments.start_date

            self._write_flow_to(flow, FileFormats.HDG, arguments.output_file)
            self._display.conversion_complete(arguments)

        except IOError as e:
            self._display.input_file_not_found(arguments, e)

    def _read_flow_from(self, file_format, path):
        with open(path, "r") as input_file:
            return self._adapters.read_from(file_format, input_file)

    def _write_flow_to(self, flow, format, path):
        with open(path, "w") as output:
            self._adapters.write_to(flow, format, output)


def main():
    """
    Entry point of the program
    """
    CLI().run(argv[1:])

