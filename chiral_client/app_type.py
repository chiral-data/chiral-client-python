import enum
from .chiral import chiral_pb2

class AppType(enum.Enum):
    Gromacs = 1

    def to_grpc_type(self) -> chiral_pb2.AppType:
        if self == AppType.Gromacs:
            return chiral_pb2.APP_GROMACS
        else:
            return chiral_pb2.APP_UNSPECIFIED
