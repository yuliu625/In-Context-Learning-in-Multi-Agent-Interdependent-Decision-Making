from __future__ import annotations
from loguru import logger

from src.agents.builders.agent_building_tools import AgentBuildingTools
from src.models.model_configs_builder import ModelConfigsBuilder
from src.agents.implements.agent_factory import AgentFactory
from src.agents.utils.json_input_processor import JsonInputProcessor

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.schemas.experiment_configs import (
        EnvironmentConfig,
        AgentConfig,
    )
    from src.agents.interfaces.ne_base_agents import NEBaseAgent
    from langchain_core.prompts import ChatPromptTemplate


class AgentBuilder:
    @staticmethod
    def batch_build_agents(
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
    ) -> dict[str, NEBaseAgent]:
        agents_model_configs = AgentBuilder.get_agents_model_configs(
            agent_configs=agent_configs,
        )
        agents = {}
        for agent_config in agent_configs:
            agents[agent_config.agent_id] = AgentBuilder.build_agent(
                environment_config=environment_config,
                agent_config=agent_config,
                model_configs=agents_model_configs[agent_config.agent_id],
            )
        agents = AgentBuilder.batch_set_agents_system_message_prompt_templates(
            agents=agents,
            environment_config=environment_config,
            agent_configs=agent_configs,
        )
        logger.info(f"Batch built {len(agents)} agents.")
        return agents

    @staticmethod
    def build_agent(
        environment_config: EnvironmentConfig,
        agent_config: AgentConfig,
        model_configs: dict,
    ) -> NEBaseAgent:
        chat_prompt_template = AgentBuildingTools.get_chat_prompt_template(
            agent_config=agent_config,
        )
        schema_pydantic_base_model = AgentBuildingTools.get_schema_pydantic_base_model(
            environment_config=environment_config,
        )
        llm = AgentBuildingTools.get_llm(
            agent_config=agent_config,
            model_configs=model_configs,
        )
        agent = AgentFactory.create_agent(
            is_reasoning=agent_config.is_reasoning,
            model_client=agent_config.model_client,
            chat_prompt_template=chat_prompt_template,
            llm=llm,
            schema_pydantic_base_model=schema_pydantic_base_model,
        )
        logger.trace(f"agent: {agent}")
        return agent

    @staticmethod
    def batch_initialize_agents(
        agents: dict[str, NEBaseAgent],
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
    ) -> dict[str, NEBaseAgent]:
        raise NotImplementedError

    @staticmethod
    def initialize_agent(
        agent: NEBaseAgent,
        environment_config: EnvironmentConfig,
        agent_config: AgentConfig,
        network_size: int,
        standalone_values: list[float],
    ) -> NEBaseAgent:
        raise NotImplementedError

    @staticmethod
    def batch_set_agents_system_message_prompt_templates(
        agents: dict[str, NEBaseAgent],
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
    ) -> dict[str, NEBaseAgent]:
        network_size = len(agent_configs)
        standalone_values = [agent_config.standalone_value for agent_config in agent_configs]
        standalone_values.sort()
        agents_ = {}
        for agent_config in agent_configs:
            agents_[agent_config.agent_id] = AgentBuilder.set_agent_system_message_prompt_template(
                agent=agents[agent_config.agent_id],
                environment_config=environment_config,
                agent_config=agent_config,
                network_size=network_size,
                standalone_values=standalone_values,
            )
        return agents_

    @staticmethod
    def set_agent_system_message_prompt_template(
        agent: NEBaseAgent,
        environment_config: EnvironmentConfig,
        agent_config: AgentConfig,
        network_size: int,
        standalone_values: list[float],
    ) -> NEBaseAgent:
        agent_ = agent.format_system_prompt_template(
            format_kwargs=dict(
                network_effect=JsonInputProcessor.put_in_markdown(
                    dict(
                        network_effect=environment_config.network_effect,
                    ),
                ),
                network_size=network_size,
                standalone_values=JsonInputProcessor.put_in_markdown(standalone_values),
                agent_attribute=JsonInputProcessor.put_in_markdown(
                    dict(
                        agent_id=agent_config.agent_id,
                        standalone_value=agent_config.standalone_value,
                    ),
                ),
            ),
        )
        logger.trace(f"Set Agent {agent_config.agent_id} chat_prompt_template: \n{agent_._chat_prompt_template}")
        logger.debug(f"Set Agent: {agent_config.agent_id}.")
        return agent_

    @staticmethod
    def batch_set_chat_prompt_templates(
        chat_prompt_templates: dict[str, ChatPromptTemplate],
        environment_config: EnvironmentConfig,
        agent_configs: list[AgentConfig],
    ) -> dict[str, ChatPromptTemplate]:
        network_size = len(agent_configs)
        standalone_values = [agent_config.standalone_value for agent_config in agent_configs]
        standalone_values.sort()
        chat_prompt_templates_ = {}
        for agent_config in agent_configs:
            chat_prompt_templates_[agent_config.agent_id] = AgentBuilder.set_chat_prompt_template(
                chat_prompt_template=chat_prompt_templates[agent_config.agent_id],
                environment_config=environment_config,
                agent_config=agent_config,
                network_size=network_size,
                standalone_values=standalone_values,
            )
        return chat_prompt_templates_

    @staticmethod
    def set_chat_prompt_template(
        chat_prompt_template: ChatPromptTemplate,
        environment_config: EnvironmentConfig,
        agent_config: AgentConfig,
        network_size: int,
        standalone_values: list[float],
    ) -> ChatPromptTemplate:
        chat_prompt_template = chat_prompt_template.partial(
            network_effect=JsonInputProcessor.put_in_markdown(
                dict(
                    network_effect=environment_config.network_effect,
                )
            ),
            network_size=network_size,
            standalone_values=JsonInputProcessor.put_in_markdown(standalone_values),
            agent_attribute=JsonInputProcessor.put_in_markdown(
                dict(
                    agent_id=agent_config.agent_id,
                    standalone_value=agent_config.standalone_value,
                ),
            ),
        )
        return chat_prompt_template

    @staticmethod
    def get_agents_model_configs(
        agent_configs: list[AgentConfig],
    ) -> dict:
        agent_model_configs = {}
        for agent_config in agent_configs:
            model_configs = agent_config.model_configs
            model_configs = ModelConfigsBuilder.add_max_retries(
                model_configs=model_configs,
                max_retries=None,
            )
            if agent_config.is_reasoning:
                model_configs = ModelConfigsBuilder.add_reasoning_kwargs(
                    model_configs=model_configs,
                    model_client=agent_config.model_client,
                )
            agent_model_configs[agent_config.agent_id] = model_configs
        rate_limiter_mapping = AgentBuildingTools.get_mapping_from_agents_to_rate_limiter(
            agent_configs=agent_configs,
        )
        for agent_config in agent_configs:
            agent_model_configs[agent_config.agent_id]['rate_limiter'] = rate_limiter_mapping[agent_config.agent_id]
        logger.trace(f"agent_model_configs: {agent_model_configs}")
        return agent_model_configs

