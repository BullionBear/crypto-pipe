import time


def delay(seconds: int):
    """
    Pauses execution for a given number of seconds, simulating a delay in a job or task.

    :param seconds: The number of seconds the function should pause execution. This should be a positive integer.
    :return: Returns the same value as the input parameter `seconds`, indicating the duration of the pause.
    """
    time.sleep(seconds)
    return seconds
