---
title: OpenAI七年沉寂后发布gpt-oss开源模型：120B参数与Apache-2.0协议
index_img: /img/cover42.png
date: 2026-07-11 22:30:00
last_modified_at: 2026-07-11 22:30:00
sticky: false
categories: 
- AI前沿
tags:
- OpenAI
- gpt-oss
- 开源模型
---

## 沉寂七年，OpenAI终于"开源"了

2025年8月5日，OpenAI在官方博客发布了一篇标题为《Introducing gpt-oss》的文章，正式推出两款全新开源权重模型：**gpt-oss-120b**（117B参数）和 **gpt-oss-20b**（21B参数）。

这是自2019年发布GPT-2以来，OpenAI首次将自家核心模型的权重对外公开。七年之久的沉默被打破，标志着开源大模型格局的重大转折。

## gpt-oss 系列：技术规格与定位

两款模型均基于 Apache 2.0 协议发布，允许自由使用、修改和商业化部署，无需向 OpenAI 支付许可费用或获取额外授权。

**gpt-oss-120b** — 旗舰级推理模型
- 参数量：约117B（基于MoE架构）
- 在多项核心基准测试中逼近甚至超越 OpenAI o4-mini 水平
- 支持高达128K token的上下文窗口
- 设计目标：深度推理、Agent任务与通用开发者场景

**gpt-oss-20b** — 轻量级模型
- 参数量：约21B
- 在同类尺寸模型中具有竞争力
- 可在消费级硬件上运行（如单张RTX 4090）

OpenAI在官方说明中表示，gpt-oss系列的三个核心设计方向是：**强大的推理能力、面向Agent的任务执行、以及灵活的开发者用例**。这与当前AI领域"大模型+工具调用+自主规划"的技术路线高度吻合。

## benchmark 表现：逼近 o3 的开源选手？

根据 OpenAI 官方公布的评测结果，gpt-oss-120b（high thinking effort）在以下基准测试中取得了令人瞩目的成绩：

| 基准测试 | gpt-oss-120b | 对比对象 |
|---------|-------------|---------|
| SWE-bench Verified | ~85% | 接近 o4-mini 水平 |
| AIME 2025 (Math) | 接近 OpenAI o3 性能 | — |
| LiveBench | 在多项子任务中领先 | — |

不过，第三方评测也揭示了模型的不足之处。Reddit r/LocalLLaMA 社区的一份分析显示，gpt-oss-120b 在 Simple-Bench（代码生成基准）上得分约22%，比 Kimi K2 低约4%。这表明虽然在推理和数学领域表现优异，但在纯粹的代码生成任务上仍有差距。

OpenAI 与 NVIDIA 合作优化了模型部署流程，使得 gpt-oss-120b 可以在单张 80GB GPU（如 A100/H100）上高效运行——这对开源模型而言是一个重要的工程突破。

## 为什么 OpenAI 此时"开源"？

OpenAI CEO Sam Altman 此前多次表示公司不会将核心模型开源，而 gpt-oss 的发布似乎与此前的公开表态存在矛盾。业内分析认为这一转变背后有多重考量：

**1. 生态竞争压力**
Meta 的 Llama 系列（当前最新版本为 Llama 4）和 Google DeepMind 的 Gemini 模型在开源领域已经形成了强大的社区生态。Hugging Face 上大量基于开源模型的微调版本，正在侵蚀 OpenAI 的商业护城河。

**2. 开发者关系管理**
长期以来，OpenAI 的 API 定价策略引发开发者的不满（尤其是 ChatGPT Plus 订阅用户无法使用高级模型）。通过提供开源权重，OpenAI 能够以"让渡部分商业利益"换取开发社区的认可——同时仍可通过 API 服务维持收入。

**3. 安全可控的开放策略**
值得注意的是，gpt-oss 采用的是"open-weight"（权重公开）而非"open-source"（代码+权重全部开源）。模型推理所需的工程代码仍在 OpenAI 手中，这意味着公司仍然保持对技术栈的控制力。

## 对开发者的实际影响

对于开发者而言，gpt-oss 的发布意味着几个重要的变化：

**本地部署成为可能。** gpt-oss-120b 可以通过 Hugging Face 直接下载权重文件，使用 vLLM、TGI 或 Ollama 等开源推理框架进行部署。Ollama 甚至在发布后数小时内就添加了模型支持。

```bash
# 通过 Ollama 运行 gpt-oss:120b
ollama run gpt-oss:120b

# 或使用 vLLM 进行高效推理
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model openai/gpt-oss-120b --port 8000
```

**降低企业使用门槛。** Apache 2.0 协议允许企业在内部部署模型而无需支付 API 费用。对于医疗、金融等数据敏感行业，本地部署意味着可以完全掌控训练数据和推理过程。

## 个人看法

OpenAI 选择在此时开源 gpt-oss，本质上是一次战略性的"以攻代守"——与其让社区用其他公司的开源模型来替代自家的产品，不如自己成为开源生态的一员，同时保留 API 服务的商业价值。

但 OpenAI 的"开源"与 Meta、Google 等公司有所不同：它更偏向于"开放权重"而非真正的 open source。开发者能拿到模型的参数权重，却拿不到完整的训练代码和数据处理流程——这意味着模型的行为仍然很大程度上依赖 OpenAI 的工程实现。

无论如何，gpt-oss 的发布标志着 AI 开源运动进入了一个新阶段：连曾经最封闭的大厂也开始拥抱开源，这将对整个行业产生深远影响。

## 参考资料

1. [OpenAI - Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/)
2. [Hugging Face - Welcome OpenAI GPT OSS](https://huggingface.co/blog/welcome-openai-gpt-oss)
3. [OpenAI GitHub Repository](https://github.com/openai/gpt-oss)
4. [arXiv - gpt-oss:120b Model Card](https://arxiv.org/html/2508.10925v1)
5. [DataRobot - Testing GPT-OSS Models](https://www.datarobot.com/blog/testing-gpt-oss-models/)
