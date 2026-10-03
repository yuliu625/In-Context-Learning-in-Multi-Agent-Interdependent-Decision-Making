from __future__ import annotations
from loguru import logger
from pydantic import BaseModel, Field, ConfigDict

from src.schemas.experiment_configs import (
    EnvironmentConfig,
    AgentConfig,
    ExperimentResult,
)
from src.schemas.interaction_protocols import EnvironmentFeedback

from langchain_core.messages import (
    AnyMessage,
    AIMessage,
)
# from langchain_core.prompts import HumanMessagePromptTemplate
import pandas as pd

from typing import TYPE_CHECKING, Callable
# if TYPE_CHECKING:
#     from langchain_core.prompts import ChatPromptTemplate
#     from langchain_core.language_models import BaseChatModel


class MASState(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    environment_config: EnvironmentConfig
    agent_configs: list[AgentConfig]
    experiment_round: int = Field(
        default=0,
    )
    chat_histories: dict[str, list[AnyMessage]] = Field(
        default_factory=dict,
    )
    last_round_structured_outputs: dict[str, dict] = Field(
        default_factory=dict,
    )
    round_environment_feedbacks: dict[str, EnvironmentFeedback] = Field(
        default_factory=dict,
    )
    results: list[ExperimentResult] = Field(
        default_factory=list,
    )

    @property
    def agent_configs_df(self) -> pd.DataFrame:
        agent_configs = [agent_config.model_dump() for agent_config in self.agent_configs]
        return pd.DataFrame(agent_configs)

