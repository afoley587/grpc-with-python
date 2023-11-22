from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MessageRequest(_message.Message):
    __slots__ = ["user_from", "chat_room", "message"]
    USER_FROM_FIELD_NUMBER: _ClassVar[int]
    CHAT_ROOM_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    user_from: str
    chat_room: str
    message: str
    def __init__(self, user_from: _Optional[str] = ..., chat_room: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class MessageReply(_message.Message):
    __slots__ = ["user_from", "chat_room", "message"]
    USER_FROM_FIELD_NUMBER: _ClassVar[int]
    CHAT_ROOM_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    user_from: str
    chat_room: str
    message: str
    def __init__(self, user_from: _Optional[str] = ..., chat_room: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class EmptyRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class StatsReply(_message.Message):
    __slots__ = ["num_messages"]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    num_messages: int
    def __init__(self, num_messages: _Optional[int] = ...) -> None: ...
