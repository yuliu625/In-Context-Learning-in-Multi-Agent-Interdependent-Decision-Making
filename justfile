# Development and experiment tasks.

# Runner can be switched to:
# - "python"
# - "uv run"
# - "docker compose run --rm research-project uv run"
runner := "uv run"

# Shared pytest flags: show output and enable DEBUG logs.
pytest_flags := "-s --log-cli-level=DEBUG"


# Default recipe: list available recipes.
default:
    @just --list

[unix]
set shell := ["bash", "-uc"]

[windows]
set shell := ["powershell.exe", "-NoProfile", "-Command"]


# Unit tests for core math and game-theory calculations.
[group('unit tests')]
test-core:
    {{runner}} pytest {{pytest_flags}} tests/unit/calculations


# Unit tests for data persistence and experiment configuration.
[group('unit tests')]
test-persistence:
    {{runner}} pytest {{pytest_flags}} tests/unit/io tests/unit/configurations


# Offline unit tests: no API key or LLM required.
[group('offline tests')]
test-offline:
    {{runner}} pytest {{pytest_flags}} tests/unit/calculations tests/unit/configurations tests/unit/fsm tests/unit/io tests/unit/prompts


# Unit tests for models. Requires API keys or an inference service.
[group('unit tests')]
test-models:
    {{runner}} pytest {{pytest_flags}} tests/unit/models


# Unit tests for base agents. Requires an LLM.
[group('unit tests')]
test-agents:
    {{runner}} pytest {{pytest_flags}} tests/unit/agents


# Online tests: agent unit tests plus integration tests. Requires an LLM.
[group('online tests')]
test-online:
    {{runner}} pytest {{pytest_flags}} tests/unit/agents tests/integration


# Run the full test suite. Requires API keys or an inference service for online tests.
[group('all tests')]
test-all:
    {{runner}} pytest {{pytest_flags}}


# Initialize experiment configurations and directories.
[group('experiments')]
setup-experiments:
    {{runner}} -m scripts.setup_experiments


# Run the configured experiments.
[group('experiments')]
run-experiments:
    {{runner}} -m scripts.run_experiments

