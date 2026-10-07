from __future__ import annotations
from loguru import logger

from langchain_core.rate_limiters import InMemoryRateLimiter

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


class RateLimiterFactory:
    @staticmethod
    def create_rate_limiter(
        model_client: Literal[
            'openai', 'google', 'anthropic', 'dashscope', 'deepseek', 'ollama',
        ],
        model_name: str,
        llm_number: int = 1,
    ) -> InMemoryRateLimiter:
        if model_client == 'openai':
            return RateLimiterFactory.create_openai_rate_limiter(
                model_name=model_name,
                llm_number=llm_number,
            )
        elif model_client == 'google':
            return RateLimiterFactory.create_google_rate_limiter(
                model_name=model_name,
                llm_number=llm_number,
            )
        elif model_client == 'anthropic':
            return RateLimiterFactory.create_anthropic_rate_limiter(
                model_name=model_name,
                llm_number=llm_number,
            )
        elif model_client == 'dashscope':
            return RateLimiterFactory.create_dashscope_rate_limiter(
                model_name=model_name,
                llm_number=llm_number,
            )
        elif model_client == 'deepseek':
            return RateLimiterFactory.create_deepseek_rate_limiter(
                model_name=model_name,
                llm_number=llm_number,
            )
        elif model_client == 'ollama':
            return RateLimiterFactory.create_local_llm_rate_limiter(
                model_name=model_name,
                llm_number=llm_number,
            )
        else:
            raise ValueError(f"Unsupported Model Client: {model_client}")

    @staticmethod
    def create_openai_rate_limiter(
        model_name: str,
        llm_number: int = 1,
    ) -> InMemoryRateLimiter:
        # free tier
        # tier 1
        if model_name.startswith((
            'gpt-3.5-turbo',
            'gpt-4',
            'gpt-4.1',
            'gpt-4o'
        )):
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=500/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=10,
            )
        elif model_name.startswith((
            'gpt-o3',
        )):
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=5000/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=10,
            )
        else:
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=500/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=10,
            )
        # tier 2
        logger.trace(f"Created OpenAI Rate Limiter: {rate_limiter}")
        return rate_limiter

    @staticmethod
    def create_google_rate_limiter(
        model_name: str,
        llm_number: int = 1,
    ) -> InMemoryRateLimiter:
        if model_name in (
            'gemini-2.5-pro',
        ):
            # free tier
            # free tier can't use gemini-2.5-pro
            # tier 1
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=150/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=10,
            )
            # tier 2
            # return InMemoryRateLimiter(
            #     requests_per_second=1000/60 / llm_number,
            #     check_every_n_seconds=0.1,
            #     max_bucket_size=10,
            # )
        elif model_name in (
            'gemini-2.5-flash',
        ):
            # free tier
            # rate_limiter = InMemoryRateLimiter(
            #     requests_per_second=10/60 / llm_number,
            #     check_every_n_seconds=0.1,
            #     max_bucket_size=10,
            # )
            # tier 1
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=1000/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=10,
            )
            # tier 2
            # rate_limiter = InMemoryRateLimiter(
            #     requests_per_second=2000/60 / llm_number,
            #     check_every_n_seconds=0.1,
            #     max_bucket_size=10,
            # )
        else:
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=10/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=10,
            )
        logger.trace(f"Created Google Rate Limiter: {rate_limiter}")
        return rate_limiter

    @staticmethod
    def create_anthropic_rate_limiter(
        model_name: str,
        llm_number: int = 1,
    ) -> InMemoryRateLimiter:
        rate_limiter = InMemoryRateLimiter(
            requests_per_second=60/60 / llm_number,
            check_every_n_seconds=0.1,
            max_bucket_size=10,
        )
        logger.trace(f"Created Anthropic Rate Limiter: {rate_limiter}")
        return rate_limiter

    @staticmethod
    def create_dashscope_rate_limiter(
        model_name: str,
        llm_number: int = 1,
    ) -> InMemoryRateLimiter:
        if model_name in (
            'qwen-max', 'qwen-max-latest',
            'qwen-turbo', 'qwen-turbo-latest',
            'qwen-long', 'qwen-long-latest',
            'qwen-vl-max', 'qwen-vl-max-latest',
            'qwen-vl-plus', 'qwen-vl-plus-latest',
        ):
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=1200/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=50,
            )
        elif model_name in (
            'qwen-plus', 'qwen-plus-latest',
        ):
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=15000/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=50,
            )
        else:
            rate_limiter = InMemoryRateLimiter(
                requests_per_second=60/60 / llm_number,
                check_every_n_seconds=0.1,
                max_bucket_size=50,
            )
        logger.trace(f"Created DashScope Rate Limiter: {rate_limiter}")
        return rate_limiter

    @staticmethod
    def create_deepseek_rate_limiter(
        model_name: str,
        llm_number: int = 1,
    ) -> InMemoryRateLimiter:
        rate_limiter = InMemoryRateLimiter(
            requests_per_second=15000/60 / llm_number,
            check_every_n_seconds=0.1,
            max_bucket_size=10,
        )
        logger.trace(f"Created DeepSeek Rate Limiter: {rate_limiter}")
        return rate_limiter

    @staticmethod
    def create_local_llm_rate_limiter(
        model_name: str,
        llm_number: int = 1,
    ) -> InMemoryRateLimiter:
        rate_limiter = InMemoryRateLimiter(
            requests_per_second=6000/60 / llm_number,
            check_every_n_seconds=0.1,
            max_bucket_size=10,
        )
        logger.trace(f"Created Local Rate Limiter: {rate_limiter}")
        return rate_limiter

