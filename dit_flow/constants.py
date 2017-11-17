from enum import Enum


class WIDGET_TYPES(Enum):
    WRITER_WIDGET = 'WriterWidget'
    READER_WIDGET = 'ReaderWidget'
    MANIPULATION_WIDGET = 'ManipulationWidget'
    UTILITY_WIDGET = 'UtilityWidget'


class RUN_MODE(Enum):
    CLI = 1
    INTERACT = 2
