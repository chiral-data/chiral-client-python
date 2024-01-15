import typing

# typing.TypeAlias requires python 3.10
TransferFile: typing.TypeAlias = typing.Tuple[str, str, str] # filename, local dir, remote dir