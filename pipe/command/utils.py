import json
import uuid
from typing import Dict, Any
from .model import Message

def make_command(command_type: str, id: str, data: Dict[str, Any]) -> Message:
    message = Message(
        cmd=command_type,
        id=id,
        data=data
    )
    message_str = message.model_dump_json()
    return message_str


def resolve_command(message_str: str) -> Message:
    message = Message.model_validate_json(message_str)
    return message
