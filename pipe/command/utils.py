import json
import uuid
from typing import Dict, Any


def make_command(command_type: str, data: Dict[str, Any]):
    message = {
        "cmd": command_type,
        "id": uuid.uuid4().hex,
        "data": data
    }
    message_str = json.dumps(message, indent=4)
    return message_str


def resolve_command(message_str: str):
    message = json.loads(message_str)
    return message
