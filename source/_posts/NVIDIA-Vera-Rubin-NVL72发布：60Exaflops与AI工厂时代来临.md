---
title: NVIDIA Vera Rubin NVL72发布：60 Exaflops算力与"AI工厂"时代的到来
cover: /img/cover42.png
date: 2026-09-13 10:00:00
categories:
- Tech前沿
tags:
- AI前沿
- NVIDIA
- AI芯片
---

## 从"卖芯片"到"卖算力工厂"：Vera Rubin 重新定义数据中心

如果说 Blackwell 让 NVIDIA 迈进了 EFLOPS（百亿亿次浮点运算）时代，那么本周在 GTC 2026 上正式亮相的 **Vera Rubin** 平台，则把整个数据中心的形态从"一堆 GPU 堆叠"升级为一座**高度集成的 AI 工厂**。

NVIDIA 官方将 Vera Rubin 定义为一个"七芯片、五机架"的 AI 超级计算机架构——它不再只是一张显卡，而是一套覆盖计算、网络、存储乃至安全的完整协同设计系统。平台已于 Q1 2026 进入全面量产阶段，合作伙伴的产品将在 2026 年下半年陆续上市。

对正在评估算力采购的企业而言，这不仅是性能参数的跃升，更是**采购与运维模式的根本转变**。

## 核心规格：单机架即是一座超级计算机

Vera Rubin NVL72 是整个平台的核心载体，其关键指标令人瞩目：

| 维度 | Vera Rubin NVL72 |
|------|------------------|
| GPU | 72 个 Rubin 芯片 + 36 个 Vera CPU |
| 推理算力 | 3.6 EFLOPS（NVFP4） |
| 训练算力 | 2.5 EFLOPS（NVFP4） |
| HBM4 容量 | 20.7 TB，带宽 1.6 PB/s |
| 系统内存 | 54 TB LPDDR5X |
| NVLink 6 扩容带宽 | 260 TB/s |
| 功耗 | ~190 kW（Max Q）/ ~230 kW（Max P） |

单颗 Rubin GPU 采用 TSMC 3nm 双芯片封装，集成 **3360 亿晶体管**，配备 288 GB HBM4、带宽 22 TB/s，提供 50 PFLOPS 的 NVFP4 推理性能——相比上一代 Blackwell 提升约 5 倍。

NVIDIA 给出的最震撼数字是：一个完整的 Vera Rubin **POD（可扩展单元）可扩至 40 个机架、1,152 颗 GPU、约 20,000 个芯片封装，总算力达 60 Exaflops**。

## 七芯片协同：为什么"协同设计"才是关键

Vera Rubin 真正的革命性不在于单点性能，而在于**七个芯片的协同设计**，每个承担明确分工：

- **Rubin GPU**：负责 prefill（处理输入上下文），50 PFLOPS 推理算力。
- **Vera CPU**：NVIDIA 首款独立数据中心 CPU，88 个自定义 Arm（Armv9.2）Olympus 核心，最高 1.5 TB LPDDR5X 内存，承担编排、任务调度与 KV cache 路由。
- **Groq 3 LPU（LP30）**：源自 NVIDIA 对 Groq 的收购，专责 decode（低延迟 token 生成）。Rubin 负责 prefill、Groq 3 负责 decode 的**分离式推理架构**，让每兆瓦吞吐提升高达 35 倍。
- **NVLink 6 Switch**：单机架 260 TB/s 扩容带宽，支持网络内计算加速 MoE 路由的 all-to-all 通信。
- **ConnectX-9 SuperNIC / BlueField-4 DPU**：负责跨机架 scale-out 与网络、存储、加密卸载。BlueField-4 还引入了全新的 **CMX（Inference Context Memory Storage Platform）**，将 GPU 内存延伸至 NVMe 存储来承载 KV cache。
- **Spectrum-6 Ethernet Switch**：NVIDIA 首款采用共封装光学（CPO）的交换机，能效提升 5 倍。

```text
┌─────────────────────── Vera Rubin NVL72 Rack ───────────────────────┐
│                                                                      │
│   [Rubin GPU ×72] ←→ [NVLink 6 Switch ×9 trays] ←→ [Vera CPU ×36]  │
│        │                                                    │        │
│        └──────── Groq 3 LPU: prefill(推理输入) → decode(生成输出) ┘    │
│                                                                      │
│   HBM4: 20.7 TB (1.6 PB/s)  |  LPDDR5X: 54 TB  |  ~190-230 kW        │
└──────────────────────────────────────────────────────────────────────┘
```

## 技术解读：面向 Agentic AI 的架构转向

Vera Rubin 的设计语言清晰地指向一个趋势——**Agentic AI（智能体 AI）**。

过去的大模型推理是"一问一答"的同步模式，而智能体需要长时间、多轮、带工具调用的交互。这对 **KV cache 的管理**提出了极高要求。NVIDIA 通过两条路径应对：

1. **分离式 prefill/decode**：让 GPU 和 LPU 各司其职，decode 阶段的低延迟由 Groq 3 LPU 保证，吞吐密度大幅提升。
2. **CMX 存储扩展**：将 KV cache 从昂贵的 HBM4 延伸到 NVMe，用成本换容量——这对百万 token 上下文的智能体场景至关重要。

此外，NVIDIA 宣称 Vera Rubin 相比 Blackwell **推理性能提升 5 倍、单 token 成本降低 10 倍**，并采用 100% 液冷（45°C 进水温度），在多数气候下可实现免冷水机的免费冷却——直接回应了 AI 工厂最大的运营成本痛点：电力与散热。

## 影响与未来展望

Vera Rubin 的意义远超硬件本身：

- **部署速度革命**：整个机架组装时间从约 2 天缩短至约 2 小时，计算托盘更换仅需 5 分钟——这对"AI 工厂"的高可用性运维意义重大。
- **生态全面铺开**：AWS、Google Cloud、微软（Fairwater AI 超级工厂）、OCI、CoreWeave、Lambda 等已宣布支持；Cisco、Dell、HPE、联想、超微等 OEM 同步跟进；Anthropic、Meta、OpenAI、xAI 等实验室均在采用名单中。
- **AMD 正面迎战**：AMD 的 Helios 机架（MI400 系列）同样瞄准 2026 下半年，号称 2.9 EFLOPS FP4、31 TB HBM4——HBM4 容量比 Vera Rubin NVL72 还高 50%。数据中心芯片竞争进入白热化。
- **更远展望**：Rubin Ultra 搭配 Kyber 机架（144 GPU、600 kW、15 EFLOPS FP4）预计 2027 年下半年推出；NVIDIA 甚至发布了面向太空数据中心的 Space-1 Vera Rubin 模块，算力达 H100 的 25 倍。

**结语**：Vera Rubin 标志着 AI 基础设施正式从"堆芯片"迈向"建工厂"。当算力、网络、存储、散热被整合进一个可快速部署的单机架单元时，采购者购买的不再是硬件规格表，而是**开箱即用的推理产能**。对于所有构建智能体应用的企业，2026 下半年将是一个关键的窗口期——是继续用 Blackwell 余温追赶，还是拥抱 Vera Rubin 的"AI 工厂"范式，答案或许很快见分晓。
