# Recursive Reasoning or Statistical Extrapolation? In-Context Learning in Multi-Agent Interdependent Decision-Making

[![Conference](https://img.shields.io/badge/EMNLP%202026-Findings-blue.svg?style=flat)](#)
[![arXiv](https://img.shields.io/badge/ArXiv-2609.18591-b31b1b.svg?style=flat&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.18591)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github)](https://github.com/yuliu625/In-Context-Learning-in-Multi-Agent-Interdependent-Decision-Making)
[![License](https://img.shields.io/github/license/yuliu625/In-Context-Learning-in-Multi-Agent-Interdependent-Decision-Making?style=flat&label=LICENSE)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/yuliu625/In-Context-Learning-in-Multi-Agent-Interdependent-Decision-Making/ci.yaml?branch=main&style=flat)](https://github.com/yuliu625/In-Context-Learning-in-Multi-Agent-Interdependent-Decision-Making/actions/workflows/ci.yaml)

Accepted to **Findings of EMNLP 2026** (to appear). 


## Abstract

In-context learning (ICL) enables large language model (LLM) agents to improve decisions using interaction history, yet it remains unclear whether such improvement reflects refined internal reasoning or mere extrapolation of statistical patterns. To disentangle these mechanisms, we study LLM agents in multi-agent incomplete-information games that require recursive belief reasoning. By constructing a public goods game and manipulating the statistical structure of historical feedback, we evaluate decision quality against a history-independent rational expectations equilibrium (REE) benchmark. Our experiments reveal that when historical statistical patterns are disrupted, the benefits of longer context largely vanish, degrading decision quality to the no-context baseline in a way sharply amplified by stronger strategic interdependence. These results suggest that, in such strategic environments, ICL behavior is more consistent with statistical extrapolation than with strategic reasoning. Our work extends the mechanistic study of ICL to strategic multi-agent settings, introduces REE as a diagnostic tool for distinguishing reasoning from extrapolation, and provides a reusable framework for probing the boundaries of LLM reasoning in recursive belief tasks.

