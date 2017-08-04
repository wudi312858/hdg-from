#
# hdg-from -- Generate HDG files for GEMSS
#
# Copyright (C) 2017 Di WU
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


class FileFormats:
    SWMM = "SWMM"
    HDG = "HDG"

    _ALL_FORMATS = [ SWMM,
                     HDG ]

    ERROR_UNKNOWN_FORMAT = "Unknown file format '{name}'."

    @staticmethod
    def match(name):
        for any_format in FileFormats._ALL_FORMATS:
            if name.upper() == any_format:
                return any_format

        error = FileFormats.ERROR_UNKNOWN_FORMAT.format(name=name)
        raise ValueError(error)


class Processor:

    def __init__(self, file_format):
        self._file_format = file_format

    def accepts(self, file_format):
        return self._file_format == file_format


class Reader(Processor):
    """
    Read a flow from a specific file format
    """

    def __init__(self, format):
        super().__init__(format)

    def read_from(self, input_stream):
        pass


class SWMMReader(Reader):
    """
    Reader from a SWMM text file
    """

    def __init__(self):
        super().__init__(FileFormats.SWMM)

    def read_from(self, input_stream):
        return None


class Writer(Processor):

    def __init__(self, format):
        super().__init__(format)

    def write_to(self, flow, output_stream):
        pass


class HDGWriter(Writer):

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

    def __init__(self):
        super().__init__(FileFormats.HDG)

    def write_to(self, flow, output_stream):
        output_stream.write(self.HDG_OUTPUT)


class AdapterLibrary:
    """
    Select the proper reader (resp. writer), depending on the given format
    and delegates the reading (resp. pretty-prining).
    """

    ERROR_NO_READER = "Reading {format} files are not yet supported"
    ERROR_NO_WRITING = "Writing {format} files are not yet supported"

    DEFAULT_READERS = [ SWMMReader() ]
    DEFAULT_WRITERS = [ HDGWriter() ]

    def __init__(self, readers=None, writers=None):
        self._readers = readers or self.DEFAULT_READERS
        self._writers = writers or self.DEFAULT_WRITERS

    def read_from(self, file_format, input_stream):
        reader = self._find_reader_for(file_format)
        return reader.read_from(input_stream)

    def _find_reader_for(self, file_format):
        for any_reader in self._readers:
            if any_reader.accepts(file_format):
                return any_reader

        error = self.ERROR_NO_READER.format(format=file_format)
        raise RuntimeError(error)

    def write_to(self, flow, file_format, output_stream):
        writer = self._find_writer_for(file_format)
        writer.write_to(flow, output_stream)

    def _find_writer_for(self, file_format):
        for any_writer in self._writers:
            if any_writer.accepts(file_format):
                return any_writer

        error = self.ERROR_NO_WRITER.format(format=file_format)
        raise RuntimeError(error)
