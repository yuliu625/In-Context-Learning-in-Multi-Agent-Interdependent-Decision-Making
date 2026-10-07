from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from langchain_core.rate_limiters import BaseRateLimiter


class ModelConfigsBuilder:
    @staticmethod
    def build_model_configs(
        model_configs: dict,
        max_retries: int | None,
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        rate_limiter: BaseRateLimiter | None = None,
    ) -> dict:
        model_configs = ModelConfigsBuilder.add_max_retries(
            model_configs=model_configs,
            max_retries=max_retries,
        )
        model_configs = ModelConfigsBuilder.add_reasoning_kwargs(
            model_configs=model_configs,
            model_client=model_client,
        )
        model_configs = ModelConfigsBuilder.add_rate_limiter(
            model_configs=model_configs,
            rate_limiter=rate_limiter,
        )
        return model_configs

    @staticmethod
    def add_rate_limiter(
        model_configs: dict,
        rate_limiter: BaseRateLimiter | None = None,
    ) -> dict:
        model_configs_ = model_configs.copy()
        model_configs_['rate_limiter'] = rate_limiter
        logger.trace(f"Added Rate Limiter: {model_configs_}")
        return model_configs_

    @staticmethod
    def add_max_retries(
        model_configs: dict,
        max_retries: int | None = None,
    ) -> dict:
        model_configs_ = model_configs.copy()
        model_configs_['max_retries'] = max_retries or 10
        logger.trace(f"Added Max Retry: {model_configs_}")
        return model_configs_

    @staticmethod
    def add_normal_kwargs(
        model_configs: dict,
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
    ) -> dict:
        model_configs_ = model_configs.copy()
        if model_client == 'openai':
            pass
        elif model_client == 'google':
            pass
            # model_configs_.setdefault('transport', 'rest')
        elif model_client == 'anthropic':
            pass
        elif model_client == 'dashscope':
            pass
        elif model_client == 'deepseek':
            pass
        elif model_client == 'ollama':
            pass
        else:
            raise ValueError(f"Unsupported Model Client: {model_client}")
        logger.trace(f"Added Normal LLM kwargs: {model_configs_}")
        return model_configs_

    @staticmethod
    def add_reasoning_kwargs(
        model_configs: dict,
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
    ) -> dict:
        model_configs_ = model_configs.copy()
        if model_client == 'openai':
            model_configs_.setdefault('reasoning_effort', 'medium')
        elif model_client == 'google':
            model_configs_.setdefault('include_thoughts', True)
            model_configs_.setdefault('thinking_budget', -1)
        elif model_client == 'anthropic':
            model_configs_.setdefault('thinking', dict(type='enabled', budget_tokens=2000))
        elif model_client == 'dashscope':
            model_configs_.setdefault('streaming', True)
            model_configs_.setdefault('model_kwargs', dict()).setdefault('enable_thinking', True)
        elif model_client == 'deepseek':
            pass
        elif model_client == 'ollama':
            model_configs_.setdefault('reasoning', True)
        else:
            raise ValueError(f"Unsupported Model Client: {model_client}")
        logger.trace(f"Added Reasoning LLM kwargs: {model_configs_}")
        return model_configs_

