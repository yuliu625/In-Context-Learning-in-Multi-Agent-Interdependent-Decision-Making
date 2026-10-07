from __future__ import annotations
from loguru import logger

from src.prompts.safe_format_message_prompt_template import safe_format_message_prompt_template
from src.agents.utils.json_input_processor import JsonInputProcessor

from typing import TYPE_CHECKING, cast
if TYPE_CHECKING:
    from src.schemas.mas_state import MASState
    from src.schemas.experiment_configs import (
        EnvironmentConfig,
        AgentConfig,
    )
    from langchain_core.runnables import RunnableConfig
    from langchain_core.messages import (
        HumanMessage,
        AnyMessage,
    )
    from langchain_core.prompts import HumanMessagePromptTemplate


class MASInitializer:
    def __init__(
        self,
        message_prompt_templates: dict[str, HumanMessagePromptTemplate],
    ):
        self.message_prompt_templates = message_prompt_templates
        logger.debug(f"message_prompt_templates: {message_prompt_templates}")

    def process_state(
        self,
        state: MASState,
        config: RunnableConfig,
    ) -> dict:
        logger.info("Experiment Start.")
        if state.experiment_round == 0:
            chat_histories = MASInitializer.initialize_environment_message(
                message_prompt_templates=self.message_prompt_templates,
                environment_config=state.environment_config,
                agent_configs=state.agent_configs,
                experiment_round=0,
            )
            fields_to_update = dict(
                chat_histories=chat_histories,
            )
            logger.debug(f"Update Fields: {fields_to_update}")
            return fields_to_update
        else:
            fields_to_update = MASInitializer.check_experiment_round(
                chat_histories=state.chat_histories,
                agent_configs=state.agent_configs,
                environment_config=state.environment_config,
                experiment_round=state.experiment_round,
            )
            logger.debug(f"Update Fields: {fields_to_update}")
            return fields_to_update

    @staticmethod
    def initialize_environment_message(
        message_prompt_templates: dict[str, HumanMessagePromptTemplate],
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
        experiment_round: int,
    ) -> dict[str, list[HumanMessage]]:
        price = environment_config.prices[experiment_round]
        environment_messages = {}
        for agent_config in agent_configs:
            environment_message = safe_format_message_prompt_template(
                message_prompt_templates=[message_prompt_templates[agent_config.agent_id]],
                format_kwargs=dict(
                    environment_feedback=None,
                    experiment_round=experiment_round,
                    price=JsonInputProcessor.put_in_markdown(
                        dict(
                            price=price,
                        ),
                    ),
                ),
            )
            environment_message = cast('list[HumanMessage]', environment_message)
            environment_messages[agent_config.agent_id] = environment_message
        logger.trace(f"environment_messages: {environment_messages}")
        return environment_messages

    @staticmethod
    def check_experiment_round(
        chat_histories: dict[str, list[AnyMessage]],
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
        experiment_round: int,
    ) -> dict:
        raise NotImplementedError

