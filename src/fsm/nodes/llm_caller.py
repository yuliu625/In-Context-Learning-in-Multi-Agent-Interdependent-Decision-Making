from __future__ import annotations
import asyncio
from loguru import logger

from src.configs import (
    MAX_CONCURRENCY,
    IS_BATCH_CALL,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.mas_state import MASState
    from src.schemas.interaction_protocols import AgentResponse
    from src.agents.interfaces.ne_base_agents import NEBaseAgent
    from langchain_core.runnables import RunnableConfig
    from langchain_core.prompts import HumanMessagePromptTemplate
    from langchain_core.messages import AnyMessage, AIMessage, HumanMessage


class LLMCaller:
    def __init__(
        self,
        agents: dict[str, NEBaseAgent],
    ):
        self.agents = agents
        logger.trace(f"agents: {agents}")

    async def process_state(
        self,
        state: MASState,
        config: RunnableConfig,
    ) -> dict:
        if IS_BATCH_CALL:
            agent_responses = await LLMCaller.batch_call_agents(
                agents=self.agents,
                chat_histories=state.chat_histories,
                max_concurrency=MAX_CONCURRENCY,
                chat_history_length=state.environment_config.chat_history_length,
            )
        else:
            agent_responses = await LLMCaller.call_agents_in_order(
                agents=self.agents,
                chat_histories=state.chat_histories,
                chat_history_length=state.environment_config.chat_history_length,
            )
        chat_histories = LLMCaller.update_chat_histories(
            messages=agent_responses['agent_messages'],
            chat_histories=state.chat_histories,
        )
        fields_to_update = dict(
            chat_histories=chat_histories,
            last_round_structured_outputs=agent_responses['structured_outputs'],
        )
        logger.debug(f"Update Fields: {fields_to_update}")
        return fields_to_update

    @staticmethod
    async def batch_call_agents(
        agents: dict[str, NEBaseAgent],
        chat_histories: dict[str, list[AnyMessage]],
        max_concurrency: int,
        chat_history_length: int,
    ) -> dict[str, dict[str, AIMessage | dict]]:
        semaphore = asyncio.Semaphore(max_concurrency)
        tasks = []
        for agent_id, agent in agents.items():
            task = LLMCaller.a_call_agent(
                agent_id=agent_id,
                agent=agent,
                chat_history=chat_histories[agent_id][-chat_history_length:],
                semaphore=semaphore,
            )
            tasks.append(task)
        agent_responses_with_id: tuple[dict] = await asyncio.gather(*tasks)
        logger.trace(f"agent_responses_with_id: {agent_responses_with_id}")
        await asyncio.sleep(10)
        agent_messages = {}
        structured_outputs = {}
        for agent_response_with_id in agent_responses_with_id:
            agent_id: str = agent_response_with_id['agent_id']
            agent_response: AgentResponse = agent_response_with_id['agent_response']
            ai_message: AIMessage = agent_response.ai_message
            structured_output: dict = agent_response.structured_output
            agent_messages[agent_id] = ai_message
            structured_outputs[agent_id] = structured_output
        agent_responses = dict(
            agent_messages=agent_messages,
            structured_outputs=structured_outputs,
        )
        logger.trace(f"agent_responses: {agent_responses}")
        return agent_responses

    @staticmethod
    async def call_agents_in_order(
        agents: dict[str, NEBaseAgent],
        chat_histories: dict[str, list[AnyMessage]],
        chat_history_length: int,
    ) -> dict[str, dict[str, AIMessage | dict]]:
        raise NotImplementedError

    @staticmethod
    async def a_call_agent(
        agent_id: str,
        agent: NEBaseAgent,
        chat_history: list[AnyMessage],
        semaphore: asyncio.Semaphore,
    ) -> dict:
        async with semaphore:
            agent_response = await agent.a_get_agent_response(
                chat_history=chat_history,
            )
            return dict(
                agent_id=agent_id,
                agent_response=agent_response,
            )

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

