from __future__ import annotations
from loguru import logger

from src.agents.implements.normal_agents import (
    NormalOpenAIAgent,
    NormalGoogleAgent,
    NormalAnthropicAgent,
    NormalDashScopeAgent,
    NormalDeepSeekAgent,
    NormalOllamaAgent,
)

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from src.agents.interfaces.ne_base_agents import NEBaseAgent
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.language_models import BaseChatModel
    from pydantic import BaseModel


class NormalAgentFactory:
    @staticmethod
    def create_normal_agent_with_model_client(
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        if model_client == 'openai':
            return NormalAgentFactory.create_normal_openai_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'google':
            return NormalAgentFactory.create_normal_google_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'anthropic':
            raise NotImplementedError
            return NormalAgentFactory.create_normal_anthropic_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'dashscope':
            return NormalAgentFactory.create_normal_dashscope_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'deepseek':
            return NormalAgentFactory.create_normal_deepseek_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        elif model_client == 'ollama':
            return NormalAgentFactory.create_normal_ollama_agent(
                chat_prompt_template=chat_prompt_template,
                llm=llm,
                schema_pydantic_base_model=schema_pydantic_base_model,
            )
        else:
            raise ValueError(f"Unsupported Model Client: {model_client}")

    @staticmethod
    def create_normal_openai_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        normal_openai_agent = NormalOpenAIAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Normal OpenAI Agent.")
        return normal_openai_agent

    @staticmethod
    def create_normal_google_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        normal_google_agent = NormalGoogleAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Normal Google Agent.")
        return normal_google_agent

    @staticmethod
    def create_normal_anthropic_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        normal_anthropic_agent = NormalAnthropicAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Normal Anthropic Agent.")
        return normal_anthropic_agent

    @staticmethod
    def create_normal_dashscope_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        normal_dashscope_agent = NormalDashScopeAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Normal DashScope Agent.")
        return normal_dashscope_agent

    @staticmethod
    def create_normal_deepseek_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        normal_deepseek_agent = NormalDeepSeekAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Normal DeepSeek Agent.")
        return normal_deepseek_agent

    @staticmethod
    def create_normal_ollama_agent(
        chat_prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
        schema_pydantic_base_model: type[BaseModel],
    ) -> NEBaseAgent:
        normal_ollama_agent = NormalOllamaAgent(
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.debug(f"Created Normal Ollama Agent.")
        return normal_ollama_agent

