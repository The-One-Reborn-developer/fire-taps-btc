import random


async def waiting_time() -> int:
    """
    Generates a random waiting time in seconds.

    The waiting time is a random integer between 5 and 20.

    Returns:
        int: The randomly generated waiting time in seconds.
    """
    return random.randint(5, 20)
