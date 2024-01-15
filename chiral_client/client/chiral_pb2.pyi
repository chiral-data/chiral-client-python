from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReplyUserCancelJob(_message.Message):
    __slots__ = ["error", "success"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: str
    success: bool
    def __init__(self, success: bool = ..., error: _Optional[str] = ...) -> None: ...

class ReplyUserGetJobStatus(_message.Message):
    __slots__ = ["error", "statuses", "success"]
    class StatusesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: str
    statuses: _containers.ScalarMap[str, str]
    success: bool
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., statuses: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ReplyUserInitialize(_message.Message):
    __slots__ = ["error", "settings", "success"]
    class SettingsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: str
    settings: _containers.ScalarMap[str, str]
    success: bool
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., settings: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ReplyUserSubmitJob(_message.Message):
    __slots__ = ["error", "success"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: str
    success: bool
    def __init__(self, success: bool = ..., error: _Optional[str] = ...) -> None: ...

class RequestUserCancelJob(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class RequestUserGetJobStatus(_message.Message):
    __slots__ = ["job_ids"]
    JOB_IDS_FIELD_NUMBER: _ClassVar[int]
    job_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, job_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class RequestUserInitialize(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RequestUserSubmitJob(_message.Message):
    __slots__ = ["job_ser"]
    JOB_SER_FIELD_NUMBER: _ClassVar[int]
    job_ser: str
    def __init__(self, job_ser: _Optional[str] = ...) -> None: ...
