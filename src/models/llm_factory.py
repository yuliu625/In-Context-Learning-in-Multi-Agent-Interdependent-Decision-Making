from __future__ import annotations
from loguru import logger

from .base_llm_factory import BaseLLMFactory
from .rate_limiter_factory import RateLimiterFactory

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class LLMFactory:
    @staticmethod
    def create_llm(
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        if model_client == 'openai':
            return LLMFactory.create_openai_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'google':
            return LLMFactory.create_google_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'anthropic':
            return LLMFactory.create_anthropic_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'dashscope':
            return LLMFactory.create_dashscope_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'deepseek':
            return LLMFactory.create_deepseek_llm(
                model_name=model_name,
                model_configs=model_configs,
            )
        elif model_client == 'ollama':
            return LLMFactory.create_ollama_llm(
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
        default_model_configs = dict(
            rate_limiter=RateLimiterFactory.create_openai_rate_limiter(
                model_name=model_name,
                llm_number=50,
            ),
            max_retries=10,
        )
        model_configs = {**default_model_configs, **(model_configs or {})}
        llm = BaseLLMFactory.create_openai_llm(
            model_name=model_name,
            model_configs=model_configs,
        )
        return llm

    @staticmethod
    def create_google_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        default_model_configs = dict(
            rate_limiter=RateLimiterFactory.create_google_rate_limiter(
                model_name=model_name,
                llm_number=50,
            ),
            max_retries=10,
        )
        model_configs = {**default_model_configs, **(model_configs or {})}
        llm = BaseLLMFactory.create_google_llm(
            model_name=model_name,
            model_configs=model_configs,
        )
        return llm

    @staticmethod
    def create_anthropic_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        default_model_configs = dict(
            rate_limiter=RateLimiterFactory.create_anthropic_rate_limiter(
                model_name=model_name,
                llm_number=50,
            ),
            max_retries=10,
        )
        model_configs = {**default_model_configs, **(model_configs or {})}
        llm = BaseLLMFactory.create_anthropic_llm(
            model_name=model_name,
            model_configs=model_configs,
        )
        return llm

    @staticmethod
    def create_dashscope_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        default_model_configs = dict(
            rate_limiter=RateLimiterFactory.create_dashscope_rate_limiter(
                model_name=model_name,
                llm_number=50,
            ),
            max_retries=10,
        )
        model_configs = {**default_model_configs, **(model_configs or {})}
        llm = BaseLLMFactory.create_dashscope_llm(
            model_name=model_name,
            model_configs=model_configs,
        )
        return llm

    @staticmethod
    def create_deepseek_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        default_model_configs = dict(
            rate_limiter=RateLimiterFactory.create_deepseek_rate_limiter(
                model_name=model_name,
                llm_number=50,
            ),
            max_retries=10,
        )
        model_configs = {**default_model_configs, **(model_configs or {})}
        llm = BaseLLMFactory.create_deepseek_llm(
            model_name=model_name,
            model_configs=model_configs,
        )
        return llm

    @staticmethod
    def create_ollama_llm(
        model_name: str,
        model_configs: dict | None = None,
    ) -> BaseChatModel:
        default_model_configs = dict(
            rate_limiter=None,
            max_retries=10,
        )
        model_configs = {**default_model_configs, **(model_configs or {})}
        llm = BaseLLMFactory.create_ollama_llm(
            model_name=model_name,
            model_configs=model_configs,
        )
        return llm

