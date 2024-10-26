import random


async def rubles(level: int) -> float:
    """
    Generates a random amount of Bitcoin based on the user's level.

    Args:
        level (int): The level of the user, which influences the BTC amount.

    Returns:
        float: The randomly generated Bitcoin amount rounded to two decimal places.

    Level 1 generates a random BTC amount between 0.5 and 30.
    Level 2 generates a random BTC amount between 0.5 and 15.
    Level 3 has a 5% chance to generate a random BTC amount between 10 and 30,
    otherwise, it generates a random BTC amount between 0.01 and 10.
    """
    try:
        if level == 1:
            return round(random.uniform(0.5, 30), 2)
        elif level == 2:
            return round(random.uniform(0.5, 15), 2)
        elif level == 3:
            if random.random() < 0.05:
                return round(random.uniform(10, 30), 2)
            else:
                return round(random.uniform(0.01, 10), 2)
    except Exception as e:
        print(f'Error generating rubles: {e}')