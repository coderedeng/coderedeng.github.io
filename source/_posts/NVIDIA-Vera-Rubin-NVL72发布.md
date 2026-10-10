---
title: NVIDIA Vera Rubin NVL72 正式发布：6 颗新芯片拼出 AI 超级计算机
cover: /img/cover42.png
date: 2026-10-10 10:00:00
categories:
- Tech前沿
tags:
- AI芯片
- NVIDIA
- Rubin
---

## 从"卖 GPU"到"造超级计算机"

NVIDIA 在 CES 2026 上正式拉开下一代 AI 计算的序幕，一次性发布以 **Vera Rubin** 为名的六大新芯片——Rubin GPU、Vera CPU、NVLink 6 Switch、ConnectX-9 SuperNIC、BlueField-4 DPU 与 Spectrum-6 Ethernet Switch。这不是又一款迭代显卡，而是把整个数据中心重新打包成一台"AI 超级计算机"的系统级宣言。目前 Rubin 已全面投产（GTC Taipei 2026 年 6 月确认），AWS、Google Cloud、Microsoft、Oracle 及 CoreWeave、Lambda 等云厂商将在 2026 下半年推出基于 Rubin 的实例。

黄仁勋的定义很直白：AI 训练与推理的需求正在"冲顶"，NVIDIA 沿袭每年推一代 AI 超级计算机的节奏，用六颗芯片的"极端协同设计"（extreme codesign）把成本打下来。

## 核心规格：带宽才是代差关键

单颗 Rubin GPU 采用台积电 3nm（3NP）工艺，集成 **3360 亿晶体管**（Blackwell 的 B200 为 2080 亿），搭载 **288GB HBM4** 显存，带宽高达 **22 TB/s**。算力方面，Rubin 单卡给出 **50 PFLOPS NVFP4 推理 / 35 PFLOPS 训练**——相比 Blackwell 的约 10 PFLOPS，推理性能直接拉到 **5 倍**，训练约 3.5 倍。

但真正拉开代差的是带宽而非算力。Blackwell 的 HBM3e 只有 8 TB/s，Rubin 的 HBM4 达到 22 TB/s，约为其 **2.75 倍**。NVIDIA 这一代有意把更多资源倾斜到内存带宽上——这与过去两代"重算力轻带宽"的方向恰好相反，也说明在推理时代，**数据搬运才是真正的瓶颈**。

 rack 层面，**Vera Rubin NVL72** 将 72 颗 Rubin GPU 与 36 颗 Vera CPU 整合进一台液冷机柜：

```
Vera Rubin NVL72（单机柜）
├─ 72 × Rubin GPU      → 3,600 PFLOPS NVFP4 推理
├─ 36 × Vera CPU       → 3,168 颗 Olympus 核心 (Arm 兼容)
├─ HBM4 总量 20.7 TB   → 1,580 TB/s 带宽
└─ NVLink 6 上行带宽    → 260 TB/s（机柜内）
```

对比上代 GB200 NVL72，NVL72 的推理算力提升约 **2.5 倍**，内存带宽约 **2.4 倍**，总 HBM 从 13.4TB 增至 20.7TB。官方给出的商业结论更诱人：**训练 MoE 模型所需 GPU 数量减少 4 倍，推理单 token 成本降低最多 10 倍**。

## Vera CPU：NVIDIA 第一次自己造 CPU

Rubin 之外，另一处结构性变化是 **Vera CPU**——NVIDIA 首款独立数据中心 CPU。它采用自研 **Olympus** Arm 兼容核心（Armv9.2），每颗 88 核、176 线程，最高支持 1.5TB LPDDR5X，通过 NVLink-C2C 提供 1.8 TB/s 的相干带宽。黄仁勋甚至直言这块 CPU"注定会成为数百亿美元级别的业务"。

在 NVL72 里 GPU 们本就是一台机器，CPU 的职责是喂数据、拆任务——而这次这个岗位不是变小，而是变大了。

## 面向 Agent AI 的新设计：Rubin CPX 与上下文存储

推理分为 prefill（吃长 prompt）和 decode（逐 token 生成）两阶段：prefill 算力受限，decode 带宽受限。让两者挤在同一块昂贵的 HBM 卡上，等于在某一个阶段浪费硅片。NVIDIA 为此推出 **Rubin CPX**——一块用更便宜的 GDDR7（每芯片 128GB）、专注计算密度的独立芯片，prefill 阶段注意力吞吐约为 GB300 的 3 倍。

打包进 **NVL144 CPX** 机柜（144 颗 Rubin CPX + 144 颗普通 Rubin GPU + 36 颗 Vera CPU）后，系统提供 **8 EFLOPS NVFP4** 算力、100TB 高速内存与 1.7 PB/s 带宽——NVIDIA 称其 AI 性能是 GB300 NVL72 的 **7.5 倍**。

同时亮相的还有 **Inference Context Memory Storage Platform**（基于 BlueField-4），用于在超大规模下共享、复用 KV cache，直接服务于多轮 Agent 推理；以及面向机密计算的 ASTRA 信任架构和采用共封装光学的 Spectrum-X Ethernet Photonics。

## 影响与展望

Rubin 的意义不在于单卡跑分，而在于它把"内存 + 互联带宽"推到了舞台中央。对云厂商和 AI 实验室而言，这意味着更长的上下文、更低延迟的多模态服务，以及真正可规模化的 Agent 推理——Anthropic、OpenAI、Meta、xAI、Microsoft、AWS 等均已宣布跟进。

路线图也已清晰：Rubin Ultra 将把性能翻倍（约 100 PFLOPS NVFP4），预计 2027 年到来；其后的 **Feynman** 则是直接继任者。对国内开发者来说，虽然高端芯片受出口管制影响，但 Rubin 所强调的"带宽优先 + CPU/GPU/网络协同设计"思路，值得在模型压缩、KV cache 优化与异构调度方向上认真借鉴。

> 参考来源：NVIDIA 官方新闻稿《NVIDIA Kicks Off the Next Generation of AI With Rubin》（CES 2026）、NVIDIA Vera Rubin NVL72 产品页、Wikipedia「Rubin (microarchitecture)」及多家硬件媒体规格分析。
