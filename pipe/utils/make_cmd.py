import pipe.const as const
from typing import Optional, Dict


def make_cmd(cmd: str, data: Optional[Dict] = None):
    if not data:
        data = {}
    return {const.CMD: cmd, const.DATA: data}
