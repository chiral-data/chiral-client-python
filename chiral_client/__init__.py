version = "0.2.1"

from .client import Client as Client
from .apps.gromacs import JobManager as GromacsJobManager
from .apps.recgen import JobManager as RecGenJobManager
from .apps.llma2 import JobManager as Llma2JobManager