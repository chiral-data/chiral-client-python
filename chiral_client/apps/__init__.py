import typing
from enum import Enum

class OperatorKind(str, Enum):
    GromacsRunGMXCommand = 'GromacsRunGMXCommand'
    ReCGenBuild = 'ReCGenBuild'
    CandleLLaMA2 = 'CandleLLaMA2'

class DatasetKind(str, Enum):
    Empty = 'Empty'

# class JobRequirement:
#     ji: str
#     opk: OperatorKind
#     dsk: DatasetKind

#     def __init__(self, input_str: str, opk: OperatorKind, dsk: DatasetKind) -> None:
#         self.ji = input_str
#         self.opk = opk
#         self.dsk = dsk
    
class CommandLineJob:
    command: str
    args: typing.List[str]
    prompts: typing.List[str]
    work_dir: str
    input_files: typing.List[str]
    output_files: typing.List[str]
    checkpoint_files: typing.List[str]

class Kind:
    run: str,
    app:     
    
class Job:
    id: str
    is_long: bool
    kind: str

