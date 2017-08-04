#
# hdg-from -- Generate HDG files for GEMSS
#
# Copyright (C) 2017 Di WU
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

from pathlib import Path
from argparse import ArgumentParser

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
            input_format=arguments.format)

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
            help="Format of the input file")
        return parser

    def __init__(self, input_file, input_format):
        self._input_file = input_file
        self._input_format = FileFormats.match(input_format)

    @property
    def input_file(self):
        return self._input_file

    @property
    def input_format(self):
        return self._input_format

    @property
    def output_file(self):
        return self._input_file.replace(".txt", ".hdg")


class CLI:
    """
    Parse the command line and then read the flow from the input file,
    and write the same flow down as an HDG file.
    """

    def __init__(self, adapters=None):
        self._adapters = adapters or AdapterLibrary()

    def run(self, command_line):
        arguments = Arguments.read_from(command_line)
        flow = self._read_flow_from(arguments.input_format, arguments.input_file)
        self._write_flow_to(flow, FileFormats.HDG, arguments.output_file)

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
    from sys import argv

    CLI().run(argv)

