---
title: MiniMind开源爆火：3块钱、2小时，从零训出你的第一只大模型
cover: /img/cover42.png
date: 2026-11-25 22:10:00
categories:
- Tech前沿
tags:
- AI前沿
- 开源项目
- LLM训练
---

最近 GitHub Trending 上最扎眼的项目，不是某个新模型，而是一句极其朴素的话："Train a 64M ChatBot from zero. 2 hours. ¥3. One 3090."——从零开始，两小时，三块钱，一张 RTX 3090。

这就是 **MiniMind**（[jingyaogong/minimind](https://github.com/jingyaogong/minimind)）。截至本周一度冲上近 70K Star，单日新增超过 1800 Star，是当下增长最快的 AI 开源项目之一。在"用 LoRA 微调一个 70B 模型只要十几行代码"成为常态的今天，这个项目偏偏反着来：把大模型的每一个环节都摊开给你看，让你亲手从 Tokenizer 一路训到 Agentic RL。

## 为什么是 MiniMind？

先说背景。过去两年，LLM 的学习路径被高度封装了：transformers、trl、peft 这些框架把"加载模型 + 加载数据 + 训练 + 推理"压缩成十几行代码，方便是方便，但也把开发者与底层实现彻底隔离开来。大多数人的经历是——调过 LoRA 的超参，却说不清注意力矩阵在干什么；跑通过 DPO 脚本，却不知道偏好损失是怎么一步步从 Bradley-Terry 模型推出来的。

作者 jingyaogong 在 README 里打了个很精彩的比方："用乐高自己拼出一架飞机，远比坐在头等舱里飞行更让人兴奋。"MiniMind 就是那盒乐高：主线最小版本体积约为 GPT-3 的 1/2700，小到一张消费级显卡就能完整跑通训练全流程，但结构上并不"玩具化"——它对齐的是 Qwen3 / Qwen3-MoE 生态的现代架构，而非过时的经典 Transformer。

## 核心特性：一条完整的"从 0 到 1"链路

MiniMind 最硬核的地方在于**全链路覆盖**。它不是只给你一个预训练脚本，而是把一条完整的大模型生产线全部开源：

- **Tokenizer 训练**：BPE + ByteLevel，自带 `<tool_call>`、`<think>` 等模板标记；
- **预训练（Pretrain）**：提供收集、蒸馏、清洗、去重后的全阶段开源数据；
- **监督微调（SFT）与 LoRA**：LoRA 脱离 peft 包装，从 0 用 PyTorch 原生实现；
- **RLHF / RLAIF**：DPO、PPO、GRPO、CISPO、SPO 全部原生实现，这是市面上极少见的小模型强化学习全家桶；
- **Agentic RL**：`train_agent.py` 支持多轮 Tool-Use 场景下的 GRPO/CISPO 训练，rollout engine 已解耦，可灵活切换生成后端；
- **自适应思考与蒸馏**：通过 `chat_template` + `<think>` 标记和 `open_thinking` 开关控制思考链，并原生实现白盒模型蒸馏（官方甚至放出过 minimind2-DeepSeek-R1 蒸馏版本）。

已发布的模型矩阵也很清晰：minimind-3（64M Dense）与 minimind-3-moe（198M-A64M MoE）为当前主线，另有 MiniMind-V（视觉）、MiniMind-O（全模态）、MiniMind-dLM（离散扩散语言模型）、MiniMind-Linear（线性注意力）等实验性分支。生态兼容性拉满：transformers / trl / peft 可训练，llama.cpp / vLLM / Ollama 可推理，还内置了兼容 OpenAI API 协议的极简服务端和 Streamlit WebUI。

上手只需要三步：

```bash
git clone --depth 1 https://github.com/jingyaogong/minimind
cd minimind && pip install -r requirements.txt

# 直接体验已训好的 64M 模型
python eval_llm.py --load_from ./minimind-3

# 或者从零开训（单卡 3090，SFT 阶段约 2 小时）
python train_sft.py
```

## 技术细节：小模型里的"大工程"

几个值得注意的工程决策。第一，**核心算法零高层抽象**。训练损失、KV-Cache、MoE 负载均衡 loss、位置编码外推（YaRN）全部手写 PyTorch，这意味着你读到的每一行代码都是可以直接复用的教学级实现，而不是对第三方库的再封装。第二，**MoE 设计紧跟前沿**：198M-A64M 的 MiniMind-3-MoE 移除了 shared expert，与 Qwen3-MoE 对齐，让学习者第一次能在小参数规模上真实体验专家路由、负载均衡辅助损失这些大模型核心机制。第三，**训练工程化程度高**：支持单机多卡 DDP/DeepSpeed、断点续训（含跨 GPU 数量恢复）、wandb/SwanLab 可视化、动态启停——这些通常只出现在工业级训练框架里的能力，在这里全部以可读代码的形式呈现。

需要说清楚的是：64M 参数的模型在通用能力上与 GPT-3 没有任何可比性，"2 小时 ¥3"指单张 3090 上 SFT 跑完 1 epoch 的实测耗时与对应租卡成本。MiniMind 的价值从来不是"训出一个能用的模型"，而是**把黑盒变成白盒**——它是目前中文社区里门槛最低、链路最完整的 LLM 训练教程级项目。

## 影响与展望

MiniMind 的爆火折射出一个清晰趋势：在开源权重模型（Qwen、DeepSeek、Kimi）和 Ollama 这类本地运行时普及之后，开发者对"模型内部如何工作"的需求正在井喷。当推理侧的成本趋近于零，训练侧的知识就成了新的分水岭——能不能理解并改造一个模型的训练流程，将决定 AI 工程师的分层。

可以预见的是，围绕 MiniMind 会出现一波社区 fork、私有数据微调变体（医疗、法律、垂直领域）以及大量教学内容的涌现。对想真正入门大模型训练的开发者来说，现在没有比"3 块钱 + 2 小时"更好的起点——毕竟，亲手从 0 训出一只属于自己的小模型，那种感受 API 永远给不了。
