from enum import Enum

WIDGET_TYPES = ['WriterWidget', 'ReaderWidget', 'ManipulationWidget']


class RUN_MODE(Enum):
    CLI = 1
    INTERACT = 2
