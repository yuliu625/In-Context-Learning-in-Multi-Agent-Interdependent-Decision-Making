from __future__ import annotations
from loguru import logger

from src.calculations.utility_calculator import UtilityParamsNameMap

import pandas as pd

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


SUM_PARTICIPANT_NUMBER_CASES = [
    (
        pd.Series(
            data=[True, False, True,],
        ),
        pd.Series(
            data=[2, 2, 2,],
        ),
    ),
]


GET_CHOICES_BY_EXPECTED_PAYOFF_CASES = [
    (
        pd.Series(
            data=[0.5, 1.3, -0.2,],
        ),
        pd.Series(
            data=[True, True, False,],
        ),
    ),
]


CALCULATE_UTILITY_CASES = [
    (
        dict(
            utility_calculating_params_df=pd.DataFrame({
                'theta': [1, 2, 3, 4, 5, 6,],
                'beta': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5,],
                'n': [3, 3, 3, 3, 3, 3,],
                'p': [5, 5, 5, 5, 5, 5,],
            }),
            utility_params_name_map=UtilityParamsNameMap(
                theta='theta',
                beta='beta',
                n='n',
                p='p',
            ),
        ),
        pd.Series(data=[-2.5, -1.5, -0.5, 0.5, 1.5, 2.5,])
    ),
    (
        dict(
            utility_calculating_params_df=pd.DataFrame({
                'standalone_value': [1, 2, 3, 4, 5, 6],
                'network_effect': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5,],
                'participant_number': [3, 3, 3, 3, 3, 3,],
                'price': [5, 5, 5, 5, 5, 5,],
            }),
            utility_params_name_map=UtilityParamsNameMap(
                theta='standalone_value',
                beta='network_effect',
                n='participant_number',
                p='price',
            ),
        ),
        pd.Series(
            data=[-2.5, -1.5, -0.5, 0.5, 1.5, 2.5,],
        ),
    ),
]


MASK_NO_CHOICE_CASES = [
    (
        dict(
            choice_series=pd.Series(
                data=[True, False, False,],
            ),
            payoff_series=pd.Series(
                data=[1, 1, -1,],
            ),
        ),
        pd.Series(
            data=[1, 0, 0,],
        ),
    ),
    (
        dict(
            choice_series=pd.Series(
                data=[True, False, False, False, True,],
            ),
            payoff_series=pd.Series(
                data=[1, 1, -1, 2, -3,],
            ),
        ),
        pd.Series(
            data=[1, 0, 0, 0, -3,],
        ),
    ),
]

