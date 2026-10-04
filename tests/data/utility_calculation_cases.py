from __future__ import annotations
from loguru import logger

import pandas as pd

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


CALCULATE_REAL_UTILITY_BY_EXPECTATION_CASES = [
    (
        pd.DataFrame({
            'standalone_value': [1, 2, 3, 4, 5, 6,],
            'network_effect': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5,],
            'expected_participant_number': [3, 3, 3, 3, 3, 3,],
            'price': [5, 5, 5, 5, 5, 5,],
        }),
        pd.DataFrame({
            'standalone_value': [1, 2, 3, 4, 5, 6,],
            'network_effect': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5,],
            'expected_participant_number': [3, 3, 3, 3, 3, 3,],
            'price': [5, 5, 5, 5, 5, 5,],
            'expected_payoff': [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5,],
            'choice_by_expected_payoff': [False, False, False, True, True, True,],
            'real_participant_number': [3, 3, 3, 3, 3, 3,],
            'real_payoff': [0, 0, 0, 0.5, 1.5, 2.5,],
        }),
    ),
]

