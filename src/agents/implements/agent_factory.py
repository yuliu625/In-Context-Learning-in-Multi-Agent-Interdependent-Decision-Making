from __future__ import annotations
from loguru import logger

from src.agents.implements.normal_agent_factory import NormalAgentFactory
from src.agents.implements.reasoning_agent_factory import ReasoningAgentFactory

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from src.agents.interfaces.ne_base_agents import NEBaseAgent
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.language_models import BaseChatModel
    from pydantic import BaseModel


class AgentFactory:
    @staticmethod
    def create_agent(
        is_reasoning: bool,
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        if is_reasoning:
            logger.debug(f"Creating Reasoning Agent.")
            reasoning_agent = ReasoningAgentFactory.create_reasoning_agent_with_model_client(
                model_client=model_client,
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
            return reasoning_agent
        else:
            logger.debug(f"Creating Normal Agent.")
            normal_agent = NormalAgentFactory.create_normal_agent_with_model_client(
                model_client=model_client,
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
            return normal_agent

