from __future__ import annotations
from loguru import logger

from src.schemas.mas_state import MASState

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


def is_experiment_continue(
    state: MASState,
) -> bool:
    if state.experiment_round == len(state.environment_config.prices):
        logger.trace(f"Experiment END")
        return False
    else:
        logger.trace(f"Experiment CONTINUE")
        return True

