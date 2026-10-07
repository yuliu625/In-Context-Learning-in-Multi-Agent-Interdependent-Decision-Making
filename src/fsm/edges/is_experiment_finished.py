from __future__ import annotations
from loguru import logger

from src.schemas.mas_state import MASState

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


def is_experiment_finished(
    state: MASState,
) -> bool:
    return False

