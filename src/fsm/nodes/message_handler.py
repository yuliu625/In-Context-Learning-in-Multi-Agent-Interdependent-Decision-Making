from __future__ import annotations
from loguru import logger

from src.agents.utils.json_input_processor import JsonInputProcessor
from src.prompts.safe_format_message_prompt_template import safe_format_message_prompt_template

from langchain_core.messages import HumanMessage

from typing import TYPE_CHECKING, cast
if TYPE_CHECKING:
    from src.schemas.mas_state import MASState
    from src.schemas.interaction_protocols import EnvironmentFeedback
    from langchain_core.runnables import RunnableConfig
    from langchain_core.prompts import HumanMessagePromptTemplate
    from langchain_core.messages import AnyMessage, AIMessage


class MessageHandler:
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
        logger.info(f"Round {state.experiment_round} Start.")
        environment_messages = MessageHandler.make_environment_messages(
            message_prompt_templates=self.message_prompt_templates,
            environment_feedbacks=state.round_environment_feedbacks,
            experiment_round=state.experiment_round,
            price=state.environment_config.prices[state.experiment_round],
        )
        chat_histories = MessageHandler.update_chat_histories(
            messages=environment_messages,
            chat_histories=state.chat_histories,
        )
        fields_to_update = dict(
            chat_histories=chat_histories,
        )
        logger.debug(f"Update Fields: {fields_to_update}")
        return fields_to_update

    @staticmethod
    def update_chat_histories(
        messages: dict[str, HumanMessage | AIMessage],
        chat_histories: dict[str, list[AnyMessage]],
    ) -> dict[str, list[AnyMessage]]:
        chat_histories_ = chat_histories.copy()
        for agent_id, message in messages.items():
            chat_histories_[agent_id].append(message)
        logger.trace(f"chat_histories: {chat_histories_}")
        return chat_histories_

    @staticmethod
    def make_environment_messages(
        message_prompt_templates: dict[str, HumanMessagePromptTemplate],
        environment_feedbacks: dict[str, EnvironmentFeedback],
        experiment_round: int,
        price: float,
    ) -> dict[str, HumanMessage]:
        environment_messages = {}
        for agent_id, message_prompt_template in message_prompt_templates.items():
            environment_message = safe_format_message_prompt_template(
                message_prompt_templates=[message_prompt_template],
                format_kwargs=dict(
                    environment_feedback=JsonInputProcessor.put_in_markdown(
                        environment_feedbacks[agent_id].model_dump(),
                    ),
                    experiment_round=experiment_round,
                    price=JsonInputProcessor.put_in_markdown(
                        dict(
                            price=price,
                        ),
                    ),
                ),
            )[0]
            environment_message = cast('HumanMessage', environment_message)
            environment_messages[agent_id] = environment_message
        logger.trace(f"environment_messages: {environment_messages}")
        return environment_messages

