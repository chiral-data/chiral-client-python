from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RequestUserCommunicate(_message.Message):
    __slots__ = ("serialized_request",)
    SERIALIZED_REQUEST_FIELD_NUMBER: _ClassVar[int]
    serialized_request: str
    def __init__(self, serialized_request: _Optional[str] = ...) -> None: ...

class ReplyUserCommunicate(_message.Message):
    __slots__ = ("success", "error", "serialized_reply")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_REPLY_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    serialized_reply: str
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., serialized_reply: _Optional[str] = ...) -> None: ...
