from __future__ import annotations
from loguru import logger
from pydantic import BaseModel, Field

from typing import TYPE_CHECKING, Literal
# if TYPE_CHECKING:


class StructuredOutputFormatFactory:
    @staticmethod
    def create_structured_output_format(
        schema_pydantic_base_model_name: Literal[
            'all', 'only-expectation', 'only-choice',
        ],
    ) -> type[BaseModel]:
        if schema_pydantic_base_model_name == 'all':
            return AgentStructuredOutput
        elif schema_pydantic_base_model_name == 'only-expectation':
            return OnlyExpectationStructuredOutput
        elif schema_pydantic_base_model_name == 'only-choice':
            return OnlyChoiceStructuredOutput
        else:
            raise ValueError(f"Unsupported Structured Output Format: {schema_pydantic_base_model_name}")


class AgentStructuredOutput(BaseModel):
    expected_participant_number: int
    is_participate: bool
    reason: str


class OnlyExpectationStructuredOutput(BaseModel):
    expected_participant_number: int
    reason: str


class OnlyChoiceStructuredOutput(BaseModel):
    is_participate: bool
    reason: str

