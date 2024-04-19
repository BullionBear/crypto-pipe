from .delay import delay
from .not_found import not_found

TASK_REGISTRY = {
    delay.__name__: delay,
    not_found.__name__: not_found
}
