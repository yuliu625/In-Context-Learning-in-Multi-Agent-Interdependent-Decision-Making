from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


CALCULATE_THEORETICAL_PARTICIPANT_NUMBER_CASES = [
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.25,
            price=2.24,
            is_include_self=False,
        ),
        6,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.25,
            price=2.23,
            is_include_self=False,
        ),
        6,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.25,
            price=5.24,
            is_include_self=False,
        ),
        2,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.25,
            price=5.26,
            is_include_self=False,
        ),
        1,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.25,
            price=6.01,
            is_include_self=False,
        ),
        0,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.75,
            price=4.74,
            is_include_self=False,
        ),
        6,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.75,
            price=4.73,
            is_include_self=False,
        ),
        6,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.75,
            price=5.49,
            is_include_self=False,
        ),
        3,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.75,
            price=5.99,
            is_include_self=False,
        ),
        1,
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.75,
            price=6.01,
            is_include_self=False,
        ),
        0,
    ),
]


CALCULATE_THEORETICAL_PRICES_CASES = [
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.25,
            precision=0.01,
            step=1,
            is_include_self=False,
        ),
        [2.24, 2.99, 3.74, 4.49, 5.24, 5.99,],
    ),
    (
        dict(
            thetas=[1, 2, 3, 4, 5, 6],
            beta=0.75,
            precision=0.01,
            step=1,
            is_include_self=False,
        ),
        [4.74, 4.99, 5.24, 5.49, 5.74, 5.99,],
    ),
]

