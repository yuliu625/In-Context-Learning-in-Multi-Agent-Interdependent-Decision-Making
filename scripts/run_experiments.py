from __future__ import annotations
import asyncio
import sys
from loguru import logger

from src.runners.experiment_runner import ExperimentRunner

from pathlib import Path
from omegaconf import OmegaConf
from pydantic import BaseModel

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class ExperimentTask(BaseModel):
    experiment_base_dir: str
    experiment_index_search_range: int
    name: str
    description: str


class ExperimentTasks(BaseModel):
    tasks: list[ExperimentTask]


def load_and_parse_experiment_tasks_file(
    experiment_tasks_file_path: str | Path,
) -> ExperimentTasks:
    experiment_tasks = OmegaConf.load(
        experiment_tasks_file_path,
    )
    experiment_tasks = OmegaConf.to_container(
        experiment_tasks,
        resolve=True,
        throw_on_missing=True,
    )
    experiment_tasks = ExperimentTasks.model_validate(
        experiment_tasks,
    )
    logger.info(f"Load Experiment Tasks at: {experiment_tasks_file_path}")
    return experiment_tasks


async def run_experiment_tasks(
    experiment_tasks: ExperimentTasks,
):
    for task in experiment_tasks.tasks:
        logger.info(f"Run Task: {task.experiment_base_dir}")
        await ExperimentRunner.search_and_run_unfinished_experiments(
            experiment_base_dir=task.experiment_base_dir,
            experiment_index_search_range=task.experiment_index_search_range,
        )
        logger.success(f"Finished {task.experiment_base_dir}")


async def main(
    experiment_tasks_file_path: str,
):
    experiment_tasks = load_and_parse_experiment_tasks_file(
        experiment_tasks_file_path=experiment_tasks_file_path,
    )
    await run_experiment_tasks(
        experiment_tasks=experiment_tasks,
    )
    logger.success(f"Finished Tasks: {experiment_tasks_file_path}")


if __name__ == '__main__':
    logger.remove()
    logger.add(
        sink=sys.stderr,
        level='INFO',
    )
    asyncio.run(
        main(
            experiment_tasks_file_path="./configs/experiment_tasks.yaml",
        ),
    )

