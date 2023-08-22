from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReplyAcceptJob(_message.Message):
    __slots__ = ["error", "job_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    error: str
    job_id: str
    def __init__(self, job_id: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class ReplyInitialize(_message.Message):
    __slots__ = ["error", "ftp_addr", "ftp_port", "user_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FTP_ADDR_FIELD_NUMBER: _ClassVar[int]
    FTP_PORT_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    error: str
    ftp_addr: str
    ftp_port: str
    user_id: str
    def __init__(self, ftp_addr: _Optional[str] = ..., ftp_port: _Optional[str] = ..., user_id: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class ReplyJobResult(_message.Message):
    __slots__ = ["error", "job_result"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    JOB_RESULT_FIELD_NUMBER: _ClassVar[int]
    error: str
    job_result: str
    def __init__(self, job_result: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class ReplyJobStatus(_message.Message):
    __slots__ = ["error", "statuses"]
    class StatusesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    error: str
    statuses: _containers.ScalarMap[str, str]
    def __init__(self, statuses: _Optional[_Mapping[str, str]] = ..., error: _Optional[str] = ...) -> None: ...

class RequestAcceptJob(_message.Message):
    __slots__ = ["divisor", "requirement"]
    DIVISOR_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENT_FIELD_NUMBER: _ClassVar[int]
    divisor: int
    requirement: str
    def __init__(self, requirement: _Optional[str] = ..., divisor: _Optional[int] = ...) -> None: ...

class RequestInitialize(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RequestJobResult(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class RequestJobStatus(_message.Message):
    __slots__ = ["job_ids"]
    JOB_IDS_FIELD_NUMBER: _ClassVar[int]
    job_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, job_ids: _Optional[_Iterable[str]] = ...) -> None: ...
