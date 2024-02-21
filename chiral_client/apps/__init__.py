# Deprecated V0.3.0

import typing
from enum import Enum

class OperatorKind(str, Enum):
    GromacsRunGMXCommand = 'GromacsRunGMXCommand'
    ReCGenBuild = 'ReCGenBuild'
    CandleLLaMA2 = 'CandleLLaMA2'

class DatasetKind(str, Enum):
    Empty = 'Empty'

class JobRequirement:
    ji: str
    opk: OperatorKind
    dsk: DatasetKind

    def __init__(self, input_str: str, opk: OperatorKind, dsk: DatasetKind) -> None:
        self.ji = input_str
        self.opk = opk
        self.dsk = dsk
