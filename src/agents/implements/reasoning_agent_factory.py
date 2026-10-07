from __future__ import annotations
from loguru import logger

from src.agents.implements.reasoning_agents import (
    ReasoningOpenAIAgent,
    ReasoningGoogleAgent,
    ReasoningAnthropicAgent,
    ReasoningDashScopeAgent,
    ReasoningDeepSeekAgent,
    ReasoningOllamaAgent,
)

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from src.agents.interfaces.ne_base_agents import NEBaseAgent
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.language_models import BaseChatModel
    from pydantic import BaseModel


class ReasoningAgentFactory:
    @staticmethod
    def create_reasoning_agent_with_model_client(
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        if model_client == 'openai':
            raise NotImplementedError
            return ReasoningAgentFactory.create_reasoning_openai_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'google':
            return ReasoningAgentFactory.create_reasoning_google_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'anthropic':
            raise NotImplementedError
            return ReasoningAgentFactory.create_reasoning_anthropic_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'dashscope':
            return ReasoningAgentFactory.create_reasoning_dashscope_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'deepseek':
            return ReasoningAgentFactory.create_reasoning_deepseek_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'ollama':
            return ReasoningAgentFactory.create_reasoning_ollama_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        else:
            raise ValueError(f"Unsupported Model Client: {model_client}")

    @staticmethod
    def create_reasoning_openai_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        reasoning_openai_agent = ReasoningOpenAIAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Reasoning OpenAI Agent.")
        return reasoning_openai_agent

    @staticmethod
    def create_reasoning_google_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        reasoning_google_agent = ReasoningGoogleAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Reasoning Google Agent.")
        return reasoning_google_agent

    @staticmethod
    def create_reasoning_anthropic_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        reasoning_anthropic_agent = ReasoningAnthropicAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Reasoning Anthropic Agent.")
        return reasoning_anthropic_agent

    @staticmethod
    def create_reasoning_dashscope_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        reasoning_dashscope_agent = ReasoningDashScopeAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Reasoning DashScope Agent.")
        return reasoning_dashscope_agent

    @staticmethod
    def create_reasoning_deepseek_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        reasoning_deepseek_agent = ReasoningDeepSeekAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Reasoning DeepSeek Agent.")
        return reasoning_deepseek_agent

    @staticmethod
    def create_reasoning_ollama_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        reasoning_ollama_agent = ReasoningOllamaAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Reasoning Ollama Agent.")
        return reasoning_ollama_agent

