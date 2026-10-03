from __future__ import annotations
from loguru import logger

import pandas as pd

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


def create_empty_agent_action_df() -> pd.DataFrame:
    return pd.DataFrame()


def create_empty_environment_feedback_df() -> pd.DataFrame:
    return pd.DataFrame()


def create_empty_results_df() -> pd.DataFrame:
    return pd.DataFrame()

