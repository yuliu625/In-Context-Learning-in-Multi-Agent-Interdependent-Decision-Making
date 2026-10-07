from __future__ import annotations
from loguru import logger

import os

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class BaseLLMFactory:
    @staticmethod
    def create_llm(
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        if model_client == 'openai':
            return BaseLLMFactory.create_openai_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'google':
            return BaseLLMFactory.create_google_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'anthropic':
            return BaseLLMFactory.create_anthropic_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'dashscope':
            return BaseLLMFactory.create_dashscope_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'deepseek':
            return BaseLLMFactory.create_deepseek_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'ollama':
            return BaseLLMFactory.create_ollama_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        else:
            raise ValueError(f"Unsupported Model Client: {model_client}")

    @staticmethod
    def create_openai_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model_name=model_name,
            base_url=os.environ['OPENAI_API_BASE_URL'],
            api_key=os.environ['OPENAI_API_KEY'],
            **(model_configs or {}),
        )
        logger.debug(f"Created OpenAI LLM: {model_name}")
        logger.debug(f"OpenAI LLM Configs: {model_configs}")
        return llm

    @staticmethod
    def create_google_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            api_key=os.environ['GEMINI_API_KEY'],
            transport='rest',
            **(model_configs or {}),
        )
        logger.debug(f"Created Google LLM: {model_name}")
        logger.debug(f"Google LLM Configs: {model_configs}")
        return llm

    @staticmethod
    def create_anthropic_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(
            model_name=model_name,
            base_url=os.environ['ANTHROPIC_API_BASE_URL'],
            api_key=os.environ['ANTHROPIC_API_KEY'],
            **(model_configs or {}),
        )
        logger.debug(f"Created Anthropic LLM: {model_name}")
        logger.debug(f"Anthropic LLM Configs: {model_configs}")
        return llm

    @staticmethod
    def create_dashscope_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        from langchain_community.chat_models.tongyi import ChatTongyi
        llm = ChatTongyi(
            model_name=model_name,
            base_url=os.environ['DASHSCOPE_API_BASE_URL'],
            api_key=os.environ['DASHSCOPE_API_KEY'],
            **(model_configs or {}),
        )
        logger.debug(f"Created DashScope LLM: {model_name}")
        logger.debug(f"DashScope LLM Configs: {model_configs}")
        return llm

    @staticmethod
    def create_deepseek_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        from langchain_deepseek import ChatDeepSeek
        llm = ChatDeepSeek(
            model_name=model_name,
            api_base=os.environ['DEEPSEEK_API_BASE_URL'],
            api_key=os.environ['DEEPSEEK_API_KEY'],
            **(model_configs or {}),
        )
        logger.debug(f"Created DeepSeek LLM: {model_name}")
        logger.debug(f"DeepSeek LLM Configs: {model_configs}")
        return llm

    @staticmethod
    def create_ollama_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(
            model=model_name,
            **(model_configs or {}),
        )
        logger.debug(f"Created Ollama LLM: {model_name}")
        logger.debug(f"Ollama LLM Configs: {model_configs}")
        return llm

