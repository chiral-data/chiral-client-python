from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

APP_GROMACS: AppType
APP_UNSPECIFIED: AppType
DESCRIPTOR: _descriptor.FileDescriptor

class JobGromacs(_message.Message):
    __slots__ = ["args", "checkpoint_files", "input_files", "is_long", "output_files", "prompts", "work_dir"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINT_FILES_FIELD_NUMBER: _ClassVar[int]
    INPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    IS_LONG_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    PROMPTS_FIELD_NUMBER: _ClassVar[int]
    WORK_DIR_FIELD_NUMBER: _ClassVar[int]
    args: _containers.RepeatedScalarFieldContainer[str]
    checkpoint_files: _containers.RepeatedScalarFieldContainer[str]
    input_files: _containers.RepeatedScalarFieldContainer[str]
    is_long: bool
    output_files: _containers.RepeatedScalarFieldContainer[str]
    prompts: _containers.RepeatedScalarFieldContainer[str]
    work_dir: str
    def __init__(self, is_long: bool = ..., args: _Optional[_Iterable[str]] = ..., prompts: _Optional[_Iterable[str]] = ..., work_dir: _Optional[str] = ..., input_files: _Optional[_Iterable[str]] = ..., output_files: _Optional[_Iterable[str]] = ..., checkpoint_files: _Optional[_Iterable[str]] = ...) -> None: ...

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

class ReplyUserSubmitAppJob(_message.Message):
    __slots__ = ["error", "job_id", "success"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: str
    job_id: str
    success: bool
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., job_id: _Optional[str] = ...) -> None: ...

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

class RequestUserSubmitAppJob(_message.Message):
    __slots__ = ["app_type", "gromacs"]
    APP_TYPE_FIELD_NUMBER: _ClassVar[int]
    GROMACS_FIELD_NUMBER: _ClassVar[int]
    app_type: AppType
    gromacs: JobGromacs
    def __init__(self, app_type: _Optional[_Union[AppType, str]] = ..., gromacs: _Optional[_Union[JobGromacs, _Mapping]] = ...) -> None: ...

class RequestUserSubmitJob(_message.Message):
    __slots__ = ["job_ser"]
    JOB_SER_FIELD_NUMBER: _ClassVar[int]
    job_ser: str
    def __init__(self, job_ser: _Optional[str] = ...) -> None: ...

class AppType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
