from __future__ import annotations
from loguru import logger
from pydantic import BaseModel, Field

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class AgentAction(BaseModel):
    agent_id: str
    standalone_value: float
    network_effect: float
    price: float
    expected_participant_number: int


class EnvironmentFeedback(BaseModel):
    agent_id: str
    standalone_value: float
    network_effect: float
    price: float
    expected_participant_number: int
    expected_payoff: float
    choice_by_expected_payoff: bool
    real_participant_number: int
    real_payoff: float


class ExperimentResult(BaseModel):
    experiment_round: int
    agent_id: str
    standalone_value: float
    network_effect: float
    price: float
    expected_participant_number: int
    expected_payoff: float
    choice_by_expected_payoff: bool
    real_participant_number: int
    real_payoff: float

