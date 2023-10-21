import random
import os

MOCK_RANDOM_FIX = 11110


def random_5_digit_number():
    if os.getenv("MOCK") == "yes":
        global MOCK_RANDOM_FIX
        MOCK_RANDOM_FIX = MOCK_RANDOM_FIX + 1
        return MOCK_RANDOM_FIX
    else:
        return random.randint(10000, 99999)
