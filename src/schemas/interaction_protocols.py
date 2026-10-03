from __future__ import annotations
from loguru import logger
from pydantic import BaseModel, Field

from langchain_core.messages import AIMessage

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class AgentResponse(BaseModel):
    ai_message: AIMessage
    structured_output: dict


class EnvironmentInformationMask(BaseModel):
    network_size: bool
    network_effect: bool
    standalone_values: bool
    agent_attribute: bool


class EnvironmentFeedback(BaseModel):
    real_participant_number: int
    real_payoff: float

