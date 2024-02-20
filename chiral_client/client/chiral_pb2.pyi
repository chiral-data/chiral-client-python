from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

APP_GROMACS: AppType
APP_UNSPECIFIED: AppType
DESCRIPTOR: _descriptor.FileDescriptor
MAR_JOB_NOT_PROCESSING: MonitorActionReply
MAR_NONE: MonitorActionReply
MAR_SUCCESS: MonitorActionReply
MAT_CANCEL: MonitorActionType
MAT_GET_DETAILS: MonitorActionType
MAT_NONE: MonitorActionType
MAT_TO_QUIT: MonitorActionType

class JobCommand(_message.Message):
    __slots__ = ["args", "checkpoint_files", "input_files", "is_long", "log_files", "output_files", "proj_name", "prompts", "work_dir"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    CHECKPOINT_FILES_FIELD_NUMBER: _ClassVar[int]
    INPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    IS_LONG_FIELD_NUMBER: _ClassVar[int]
    LOG_FILES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    PROJ_NAME_FIELD_NUMBER: _ClassVar[int]
    PROMPTS_FIELD_NUMBER: _ClassVar[int]
    WORK_DIR_FIELD_NUMBER: _ClassVar[int]
    args: _containers.RepeatedScalarFieldContainer[str]
    checkpoint_files: _containers.RepeatedScalarFieldContainer[str]
    input_files: _containers.RepeatedScalarFieldContainer[str]
    is_long: bool
    log_files: _containers.RepeatedScalarFieldContainer[str]
    output_files: _containers.RepeatedScalarFieldContainer[str]
    proj_name: str
    prompts: _containers.RepeatedScalarFieldContainer[str]
    work_dir: str
    def __init__(self, work_dir: _Optional[str] = ..., proj_name: _Optional[str] = ..., is_long: bool = ..., args: _Optional[_Iterable[str]] = ..., prompts: _Optional[_Iterable[str]] = ..., input_files: _Optional[_Iterable[str]] = ..., output_files: _Optional[_Iterable[str]] = ..., checkpoint_files: _Optional[_Iterable[str]] = ..., log_files: _Optional[_Iterable[str]] = ...) -> None: ...

class JobScript(_message.Message):
    __slots__ = ["apps", "command", "script_file"]
    APPS_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FILE_FIELD_NUMBER: _ClassVar[int]
    apps: _containers.RepeatedScalarFieldContainer[AppType]
    command: JobCommand
    script_file: str
    def __init__(self, command: _Optional[_Union[JobCommand, _Mapping]] = ..., script_file: _Optional[str] = ..., apps: _Optional[_Iterable[_Union[AppType, str]]] = ...) -> None: ...

class ReplyUserGetCreditPoints(_message.Message):
    __slots__ = ["error", "points", "success"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: str
    points: float
    success: bool
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., points: _Optional[float] = ...) -> None: ...

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

class ReplyUserSendMonitorAction(_message.Message):
    __slots__ = ["error", "reply", "success"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error: str
    reply: MonitorActionReply
    success: bool
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., reply: _Optional[_Union[MonitorActionReply, str]] = ...) -> None: ...

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

class RequestUserGetCreditPoints(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RequestUserGetJobStatus(_message.Message):
    __slots__ = ["job_ids"]
    JOB_IDS_FIELD_NUMBER: _ClassVar[int]
    job_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, job_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class RequestUserInitialize(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RequestUserSendMonitorAction(_message.Message):
    __slots__ = ["action_type", "job_id"]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    action_type: MonitorActionType
    job_id: str
    def __init__(self, job_id: _Optional[str] = ..., action_type: _Optional[_Union[MonitorActionType, str]] = ...) -> None: ...

class RequestUserSubmitAppJob(_message.Message):
    __slots__ = ["gromacs", "script"]
    GROMACS_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    gromacs: JobCommand
    script: JobScript
    def __init__(self, script: _Optional[_Union[JobScript, _Mapping]] = ..., gromacs: _Optional[_Union[JobCommand, _Mapping]] = ...) -> None: ...

class RequestUserSubmitJob(_message.Message):
    __slots__ = ["job_ser"]
    JOB_SER_FIELD_NUMBER: _ClassVar[int]
    job_ser: str
    def __init__(self, job_ser: _Optional[str] = ...) -> None: ...

class AppType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class MonitorActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class MonitorActionReply(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
