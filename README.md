# Recursive Reasoning or Statistical Extrapolation? In-Context Learning in Multi-Agent Interdependent Decision-Making

[![Conference](https://img.shields.io/badge/EMNLP%202026-Findings-blue.svg?style=flat)](#)
[![arXiv](https://img.shields.io/badge/ArXiv-2609.18591-b31b1b.svg?style=flat&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.18591)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github)](https://github.com/yuliu625/In-Context-Learning-in-Multi-Agent-Interdependent-Decision-Making)
[![License](https://img.shields.io/github/license/yuliu625/In-Context-Learning-in-Multi-Agent-Interdependent-Decision-Making?style=flat&label=LICENSE)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/yuliu625/In-Context-Learning-in-Multi-Agent-Interdependent-Decision-Making/ci.yaml?branch=main&style=flat)](https://github.com/yuliu625/In-Context-Learning-in-Multi-Agent-Interdependent-Decision-Making/actions/workflows/ci.yaml)

Accepted to **Findings of EMNLP 2026** (to appear). 


## Abstract

In-context learning (ICL) enables large language model (LLM) agents to improve decisions using interaction history, yet it remains unclear whether such improvement reflects refined internal reasoning or mere extrapolation of statistical patterns. To disentangle these mechanisms, we study LLM agents in multi-agent incomplete-information games that require recursive belief reasoning. By constructing a public goods game and manipulating the statistical structure of historical feedback, we evaluate decision quality against a history-independent rational expectations equilibrium (REE) benchmark. Our experiments reveal that when historical statistical patterns are disrupted, the benefits of longer context largely vanish, degrading decision quality to the no-context baseline in a way sharply amplified by stronger strategic interdependence. These results suggest that, in such strategic environments, ICL behavior is more consistent with statistical extrapolation than with strategic reasoning. Our work extends the mechanistic study of ICL to strategic multi-agent settings, introduces REE as a diagnostic tool for distinguishing reasoning from extrapolation, and provides a reusable framework for probing the boundaries of LLM reasoning in recursive belief tasks.


## Project Structure

```text
src/
├── agents/             # Multi-Agent architectures and logic
│   ├── builders/       # Agent factory and assembly logic
│   ├── implements/     # Concrete agent implementations
│   ├── interfaces/     # Abstract interfaces and base classes
│   └── utils/          # Agent-specific utilities
├── fsm/                # Finite State Machine design
│   ├── nodes/          # State nodes definitions and logic
│   ├── edges/          # State transition definitions and logic
│   └── graphs/         # Graph topology and execution orchestration
├── calculations/       # Interdependent decision-making and payoff calculations
├── configurations/     # Configuration schemas, loaders, and management tools
├── models/             # Unified LLM provider adapters and wrappers
├── prompts/            # Prompt templates loaders and processing pipelines
├── runners/            # Experiment workflows and simulation runners
├── schemas/            # Data models and Pydantic validation schemas
├── io/                 # Data persistence and file operations
└── utils/              # Project-wide utilities
```


## Quick Start

I recommend using **devcontainer** and **uv** for development and environment management. For running the full pipeline, I recommend using **Docker Compose**.

### 1. Environment Setup

Before running or debugging the project, configure an `.env` file following the instructions in `env.example`. Do not commit your `.env` file.

### 2. Data Volume Mounting

The `./configs` and `./data` directories serve as placeholders. Before running experiments, set up your data paths using one of the following methods:

- Modify the dataset mount path in `compose.yaml`, **or**
- Symlink `./data` to your actual data storage location, **or**
- Keep the default directory structure (outputs under `./data` pre-configured to be ignored by `.gitignore` and `.dockerignore`) .

### 3. Experiment Configuration

You can build configuration files in either of the following ways:

- Refer to `./configs/experiment_control_schema.yaml` to build a config manually.
- Use `./scripts/make_experiments.py` to generate a standard config from `./configs/experiment_control_template.yaml`.

### 4. Running Experiments

The recommended way to run the project is through **Docker Compose**, using the configuration in `compose.yaml`. Convenience `just` recipes are provided:

```bash
just setup-experiments
just run-experiments
```


## Development

### Available Recipes

I use `just` to manage common development tasks and test workflows:

```text
Available recipes:
    default           # Default recipe: list available recipes.

    [all tests]
    test-all          # Run the full test suite. Requires API keys or an inference service for online tests.

    [experiments]
    run-experiments   # Run the configured experiments.
    setup-experiments # Initialize experiment configurations and directories.

    [offline tests]
    test-offline      # Offline unit tests: no API key or LLM required.

    [online tests]
    test-online       # Online tests: agent unit tests plus integration tests. Requires an LLM.

    [unit tests]
    test-agents       # Unit tests for base agents. Requires an LLM.
    test-core         # Unit tests for core math and game-theory calculations.
    test-models       # Unit tests for models. Requires API keys or an inference service.
    test-persistence  # Unit tests for data persistence and experiment configuration.
```

For complete script details, see the [`justfile`](./justfile).

