---
title: AMD Instinct MI400 系列三款新型号发布：MI455X 推理性能领先 NVIDIA Vera Rubin 约 30%
cover: /img/cover42.png
date: 2026-11-27 22:00:00
categories:
- Tech前沿
tags:
- AI芯片
- AMD
- MI400
---

## 背景

AMD 在 2026 年 7 月 23 日的 Advancing AI (AAI) 2026 活动上正式发布了新一代数据中心 GPU——Instinct MI400 系列，代号基于 5th Gen CDNA 架构（CDNA 5）。如今，在 11 月 12 日，AMD 又陆续披露了 MI400 系列的三款新动态：面向科研计算的 MI430X、在 Helios 机架级系统上完成实测的 MI455X，以及新推出的 MI450X。这一系列更新进一步巩固了 AMD 在 AI 训练/推理与高性能计算（HPC）双线并行的战略布局。

## 核心特性

### MI430X：面向高精度科研计算的“科学家 GPU”

MI430X 是 MI400 系列中对科学计算最友好的一员。它内置原生 FP64 双精度算力，配合 **432GB HBM4 显存**与**高达 23.3TB/s 显存带宽**，让科学计算与 AI for Science 应用的规模得到进一步扩容。AMD 在新研究中评估了覆盖 11 个应用/基准、共 47 种工作负载配置的 FP64 仿真情形，援助了 FP64 仿真与原生双精度计算的边界，指向 MI430X 在大规模高精度模拟中的定位。

### MI455X：Helios 机架级系统上的推理领跑者

MI455X（2nm / CDNA 5 工艺，基于 MI450 256CU 图形处理器）是面向 AI 推理、训练与微调的旗舰。AMD 性能实验室 2026 年 10 月的实测显示，MI455X 在 **DeepSeek-R1** 上以 MLPerf Inference Offline 配置单卡可达 **每秒 21,333 tokens** 的推理吞吐，较 NVIDIA Vera Rubin NVL72（MLPerf v6.1 公布的最高结果）**最高高出约 30%**。此外，AMD Helios 机架系统相比 Vera Rubin 在 HBM 带宽上高出约 20%，Scale-up 带宽也有提升，这正是其推理表现的基石。

### MI450X：满足不同内存需求的全新配置

MI450X 是 AMD 近年来最灵活的新型号之一。其 GPU 配备 **288GB HBM4**，与 MI455X 共享同样的核心计算、显存带宽以及 Scale-up/Scale-out 互联能力，但总内存基于 288GB 配置。对内存需求中等的工作负载，MI450X 提供了另一种可选择的吞吐与响应时延目标；对于更大模型、更长上下文或更高并发，则仍建议使用内存头肩更大的 MI455X。两者均运行在同一 Open Rack-scale 架构以及 ROCm 软件栈之上。

## 技术分析

从架构演进看，AMD MI400 系列展示了“一套设计、多款差异化配置”的清晰产品线策略：以 MI430X 切入科研 HPC（原生 FP64）、以 MI455X 攻击推理高吞吐（21,333 tokens/GPU）、以 MI450X 补齐内存容量灵活度。对 AMD 而言，MI450X 的诞生也印证了其对客户需求的快速响应 —— 在同一 Helios 机架平台上同时部署 MI455X 与 MI450X，既共享同样的硬件/软件栈，又让客户按负载按需选型，显著降低了 bring-up 和集成成本。

在软件层，MI400 系列依托 ROCm 生态，与 NVIDIA CUDA 形成竞争对手之势。对机架级部署而言，AMD 将 Infinity Fabric 互连与 EPYC “Venice” CPU（96 核）相结合，并行推进 Scale-up/Scale-out。与 Intel Gaudi 系列和 NVIDIA Vera Rubin 相比，AMD 的优势在于计算密度、显存带宽与价格/性能的综合权衡。

## 影响与展望

1. **推理成本优化**：MI455X 单卡 21,333 tokens/s 的实测吞吐，结合 Helios 机架系统，预期将显著压低单卡推理成本，吸引大语言模型服务与在线推理的部署方。
2. **科研 × AI 融合**：MI430X 的 FP64 + HBM4 双重加持，将 FP64 科学计算与 AI 辅助科学发现进一步推向同一平台。
3. **生态参与**：AMD 正在持续补强 Helios 平台的兼容性与生态深度，吸引 hyperscaler 与科研机构对 AMD ROCm 生态的关注。

可以预见，在 Vera Rubin 与 MI455X 之间，AI 机架级 GPU 竞争将愈演愈烈，而 MI450X 这一新型号的加入，将进一步扩大 AMD 在推理/训练市场的覆盖面。

## 参考来源

- [AMD Newsroom — AMD Advances the Instinct MI400 Series for AI and Scientific Computing (Nov 12, 2026)](https://newsroom.amd.com/news/amd-advances-instinct-mi400-series-ai-scientific-computing/)
- [AMD — Instinct MI455X GPU](https://www.amd.com/en/products/accelerators/instinct/mi400/mi455x.html)
- [ServeTheHome — AMD MI400 GPU at Hot Chips 2026](https://www.servethehome.com/amd-mi400-gpu-at-hot-chips-2026/)
- [TechPowerUp — AMD Instinct MI455X Specs](https://www.techpowerup.com/gpu-specs/instinct-mi455x.c4423)
